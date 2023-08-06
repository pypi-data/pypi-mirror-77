# Copyright (c) 2018 Zbigniew Kurzynski. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.

import os
import sys
from typing import List, Dict

import piexif
from PyQt5.QtCore import Qt, QSize, QVariant, QDateTime, \
    pyqtSignal, QModelIndex, QItemSelection, QItemSelectionModel, QThread, QSortFilterProxyModel, QAbstractItemModel, \
    QPersistentModelIndex, QItemSelectionRange
from PyQt5.QtGui import QStandardItemModel, QPixmap, QPainter, QStandardItem, QIcon, QTransform
from PyQt5.QtWidgets import QWidget, QApplication, QListView, QVBoxLayout, QAbstractItemView, QFileDialog, \
    QHBoxLayout, QDateTimeEdit, QAbstractSpinBox, QFormLayout, \
    QLabel, QProgressBar, QMessageBox, QMainWindow, QToolBar, QDialog, QGroupBox, QCheckBox, QDialogButtonBox, \
    QSizePolicy


def get_icon(file: str) -> str:
    return os.path.join(os.path.dirname(__file__), "icons", "wired", file)


class RemoveConfirmationDialog(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.setWindowTitle("Confirmation")
        self.setWindowIcon(QIcon(get_icon("icons8-delete-file.png")))
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(70, 20, 70, 20)

        self.text = QLabel("Remove selected file(s) ?")
        self.checkbox_delete_from_disk = QCheckBox("Delete from disk as well.")
        self.checkbox_delete_from_disk.setChecked(False)

        self.layout.addSpacing(20)
        self.layout.addWidget(self.text)
        self.layout.addSpacing(30)
        self.layout.addWidget(self.checkbox_delete_from_disk)
        self.layout.addSpacing(10)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        self.layout.addWidget(self.buttons)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.setLayout(self.layout)

    def is_remove_from_disk(self):
        return self.checkbox_delete_from_disk.isChecked()


class ApplyOptionDialog(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.setWindowTitle("Save options")
        self.setWindowIcon(QIcon(get_icon("icons8-save.png")))
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)

        self.checkbox_exif_digitalized = QCheckBox("Set Exif DateTimeDigitized")
        self.checkbox_exif_original = QCheckBox("Set Exif DateTimeOriginal")
        self.checkbox_file_modified = QCheckBox("Set File Date Modified")
        self.checkbox_unique_seconds = QCheckBox("Increase seconds if not unique")

        self.checkbox_exif_digitalized.setChecked(True)
        self.checkbox_exif_original.setChecked(True)
        self.checkbox_file_modified.setChecked(True)
        self.checkbox_unique_seconds.setChecked(True)

        self.layout.addWidget(self.checkbox_exif_digitalized)
        self.layout.addWidget(self.checkbox_exif_original)
        self.layout.addWidget(self.checkbox_file_modified)
        self.layout.addWidget(self.checkbox_unique_seconds)

        self.setLayout(self.layout)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.buttons)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def get_options(self):
        return (self.checkbox_exif_digitalized.isChecked(),
                self.checkbox_exif_original.isChecked(),
                self.checkbox_file_modified.isChecked(),
                self.checkbox_unique_seconds.isChecked())


class UserRolePicture:
    ExifIFD_DateTimeDigitized = Qt.UserRole + 1
    ExifIFD_DateTimeOriginal = Qt.UserRole + 2
    ImageIFD_DateTime = Qt.UserRole + 3
    TimeStamp = Qt.UserRole + 4
    CameraModel = Qt.UserRole + 5
    FileName = Qt.UserRole + 6
    CameraPictures = Qt.UserRole + 7
    LazyLoadData = Qt.UserRole + 8
    IsGPS = Qt.UserRole + 9
    RotateAngle = Qt.UserRole + 10
    IsThumbnail = Qt.UserRole + 11


class ExifStoreThread(QThread):
    EXIF_DATETIME_FORMAT: str = "yyyy:MM:dd HH:mm:ss"
    FILESYSTEM_DATETIME_FORMAT: str = "yyyy_MM_dd_HH-mm-ss"
    in_queue: List = []
    filename_changed = pyqtSignal(QPersistentModelIndex, str, QDateTime)
    exception = pyqtSignal(OSError)
    progress_max_changed = pyqtSignal(int)
    progress_changed = pyqtSignal(int)
    is_running = pyqtSignal(bool)
    set_exif_digitalized = False
    set_exif_original = False
    set_file_modified = False
    set_unique_seconds = False

    def __init__(self, ):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def append_data(self, data: (QModelIndex, str, QDateTime)):
        self.in_queue.append(data)

    def set_options(self, options):
        (self.set_exif_digitalized, self.set_exif_original, self.set_file_modified,
         self.set_unique_seconds) = options

    def run(self):
        self.is_running.emit(True)
        self.progress_changed.emit(0)
        print(f"Updating exif information in {len(self.in_queue):d} elements.")
        self.progress_max_changed.emit(len(self.in_queue))
        for idx, (model_idx, file, new_datetime) in enumerate(self.in_queue):
            new_datetime: QDateTime

            # set new file name
            dir_path, filename = os.path.split(file)
            _, ext = os.path.splitext(filename)
            counter = 0
            new_filename = "%s-%02d%s" % (new_datetime.toString(self.FILESYSTEM_DATETIME_FORMAT), counter, ext)
            if filename != new_filename:
                while os.path.exists(os.path.join(dir_path, new_filename)):
                    if self.set_unique_seconds:
                        new_datetime = new_datetime.addSecs(1)
                    else:
                        counter += 1
                    new_filename = "%s-%02d%s" % (new_datetime.toString(self.FILESYSTEM_DATETIME_FORMAT), counter, ext)
                    if filename == new_filename:
                        break

                if filename != new_filename:
                    try:
                        new_file = os.path.join(dir_path, new_filename)
                        os.renames(file, new_file)
                    except OSError as e:
                        self.exception.emit(e)

            new_file = os.path.join(dir_path, new_filename)
            # set exif attributes
            exif_dict = piexif.load(new_file)
            exif_datetime = exif_dict["Exif"].get(piexif.ExifIFD.DateTimeDigitized,
                                                  exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal, b"")).decode()

            old_datetime = QDateTime.fromString(exif_datetime, self.EXIF_DATETIME_FORMAT)
            if new_datetime != old_datetime:
                new_exif_datatime = new_datetime.toString(self.EXIF_DATETIME_FORMAT).encode()
                if self.set_exif_original:
                    exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = new_exif_datatime

                if self.set_exif_digitalized:
                    exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = new_exif_datatime
                exif_bytes = piexif.dump(exif_dict)
                piexif.insert(exif_bytes, new_file)

            # set file attributes (this action must be at the very end to take effect.
            if self.set_file_modified:
                os.utime(new_file, (new_datetime.toSecsSinceEpoch(), new_datetime.toSecsSinceEpoch()))

            self.filename_changed.emit(model_idx, new_file, new_datetime)
            self.progress_changed.emit(idx + 1)
        del self.in_queue[:]
        print("Updating exif information finished.")
        self.is_running.emit(False)


class FileRemoveThread(QThread):
    items_to_remove: List = []
    removed = pyqtSignal(QPersistentModelIndex)
    progress_max_changed = pyqtSignal(int)
    progress_changed = pyqtSignal(int)
    exception_log = []
    is_remove_from_disk = False

    def __init__(self, ):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def get_exception_log(self):
        return self.exception_log

    def set_elements_to_remove(self, indexes: List[QPersistentModelIndex]):
        self.items_to_remove = indexes

    def set_remove_from_disk(self, value):
        self.is_remove_from_disk = value

    def run(self):
        del self.exception_log[:]
        self.msleep(500)
        print("There are %d elements to delete." % len(self.items_to_remove))
        self.progress_changed.emit(0)
        self.progress_max_changed.emit(len(self.items_to_remove))
        for index, idx in enumerate(self.items_to_remove):
            file = idx.data(UserRolePicture.FileName)
            if self.is_remove_from_disk:
                try:
                    print("Removing file: {0}".format(file))
                    os.remove(file)
                except OSError as e:
                    print(e)
                    self.exception_log.append(e)
            self.removed.emit(idx)
            self.progress_changed.emit(index + 1)
        del self.items_to_remove[:]
        print("Delete process done.")


class ExifLoadThread(QThread):
    items_to_load: List = []
    images_to_fetch: List = []
    EXIF_DATETIME_FORMAT: str = "yyyy:MM:dd HH:mm:ss"
    loaded = pyqtSignal(QPersistentModelIndex, dict)
    progress_max_changed = pyqtSignal(int)
    progress_changed = pyqtSignal(int)
    timestamp_format = "yyyy-MM-dd HH:mm:ss"

    def __init__(self, ):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def set_timestamp_format(self, format: str):
        self.timestamp_format = format

    def load_item(self, idx: QPersistentModelIndex):
        self.items_to_load.append(idx)

    def create_icon(self, original_pixmap: QPixmap, rotate_deg: int, is_gps: bool) -> QIcon:
        original_pixmap = original_pixmap.transformed(QTransform().rotate(rotate_deg))
        original_pixmap = original_pixmap.scaled(QSize(256, 256), Qt.KeepAspectRatioByExpanding)
        if is_gps:
            gps_picture = QPixmap(get_icon("icons8-gps.png"))
            painter = QPainter(original_pixmap)
            painter.drawPixmap(10, 10, gps_picture)
            painter.end()
        return QIcon(original_pixmap)

    def get_exif_timestamp(self, exif_dict: Dict) -> QDateTime:
        exif_datetime = exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal,
                                              exif_dict["Exif"].get(piexif.ExifIFD.DateTimeDigitized,
                                                                    exif_dict["0th"].get(piexif.ImageIFD.DateTime,
                                                                                         b""))).decode()

        date_time = QDateTime.fromString(exif_datetime, self.EXIF_DATETIME_FORMAT)

        return date_time

    def extract_exif_data(self, file: str) -> Dict[int, QVariant]:
        data: Dict[int, QVariant] = dict()
        camera_model = "Unknown"
        thumbnail_pixmap = None
        is_thumbnail = False

        exif_dict = piexif.load(file)

        # get EXIF orientation
        rotate_deg = 0
        orientation = exif_dict["0th"].get(piexif.ImageIFD.Orientation, 0)
        if orientation == 3:
            rotate_deg = 180
        elif orientation == 6:
            rotate_deg = 90
        elif orientation == 8:
            rotate_deg = 270

        # is EXIF GPS
        is_gps = piexif.GPSIFD.GPSTimeStamp in exif_dict["GPS"]

        # get EXIF thumbnail
        th = exif_dict.pop("thumbnail")
        if th:
            thumbnail_pixmap = QPixmap()
            thumbnail_pixmap.loadFromData(th)
            is_thumbnail = True

        # get EXIF dates
        date_time = self.get_exif_timestamp(exif_dict)
        if date_time:
            data[Qt.DisplayRole] = QVariant(date_time.toString(self.timestamp_format))
            data[UserRolePicture.TimeStamp] = QVariant(date_time)
        else:
            data[Qt.DisplayRole] = QVariant("Timestamp not available")
            data[UserRolePicture.TimeStamp] = QVariant(QDateTime())

        # get EXIF camera model
        model = exif_dict["0th"].get(piexif.ImageIFD.Model, camera_model.encode()).decode()

        if thumbnail_pixmap is not None:
            data[Qt.DecorationRole] = QVariant(self.create_icon(thumbnail_pixmap, rotate_deg, is_gps))

        data[UserRolePicture.RotateAngle] = QVariant(rotate_deg)
        data[UserRolePicture.IsGPS] = QVariant(is_gps)
        data[UserRolePicture.CameraModel] = QVariant(model)
        data[UserRolePicture.FileName] = QVariant(file)
        data[UserRolePicture.IsThumbnail] = QVariant(is_thumbnail)
        data[Qt.SizeHintRole] = QVariant(QSize(260, 310))
        return data

    def run(self):
        # phase I - load exif data
        self.msleep(500)
        print("There are %d elements to load." % len(self.items_to_load))
        del self.images_to_fetch[:]
        self.progress_changed.emit(0)
        self.progress_max_changed.emit(len(self.items_to_load))
        for index, idx in enumerate(self.items_to_load):
            file = idx.data(UserRolePicture.FileName)
            data = self.extract_exif_data(file)
            self.loaded.emit(idx, data)
            self.progress_changed.emit(index + 1)
        del self.items_to_load[:]
        print("Exif loading finished.")


class FullImageLoaderThread(QThread):
    images_to_fetch: List = []
    loaded = pyqtSignal(QPersistentModelIndex, dict)
    progress_max_changed = pyqtSignal(int)
    progress_changed = pyqtSignal(int)

    def __init__(self, ):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def add_image(self, idx: QPersistentModelIndex):
        self.images_to_fetch.append(idx)

    def create_icon(self, original_pixmap: QPixmap, rotate_deg: int, is_gps: bool) -> QIcon:
        original_pixmap = original_pixmap.transformed(QTransform().rotate(rotate_deg))
        original_pixmap = original_pixmap.scaled(QSize(256, 256), Qt.KeepAspectRatioByExpanding)
        if is_gps:
            gps_picture = QPixmap(get_icon("icons8-gps.png"))
            painter = QPainter(original_pixmap)
            painter.drawPixmap(10, 10, gps_picture)
            painter.end()
        return QIcon(original_pixmap)

    def run(self):
        self.progress_changed.emit(0)
        self.progress_max_changed.emit(len(self.images_to_fetch))
        print("There are %d images to load." % len(self.images_to_fetch))
        for index, idx in enumerate(self.images_to_fetch):
            if idx.isValid():
                file = idx.data(UserRolePicture.FileName)
                rotate_angle = idx.data(UserRolePicture.RotateAngle)
                is_gps = idx.data(UserRolePicture.IsGPS)
                pixmap = QPixmap(file)
                icon = self.create_icon(pixmap, rotate_angle, is_gps)
                data: Dict[int, QVariant] = dict()
                data[Qt.DecorationRole] = QVariant(icon)
                self.loaded.emit(idx, data)
                self.progress_changed.emit(index + 1)
            else:
                print("Something went wrong, the persistent index is invalid")
        del self.images_to_fetch[:]
        print("Image loading finished.")


class JpgSorter(QMainWindow):
    DATATIME_FORMAT: str = "yyyy-MM-dd HH:mm:ss"
    exif_loader_thread = ExifLoadThread()
    exif_store_thread = ExifStoreThread()
    remove_files_thread = FileRemoveThread()
    full_image_loader_thread = FullImageLoaderThread()
    list_view: QListView = None
    camera_view = None
    sel_timestamp_prev: QDateTime = QDateTime()
    sel_timestamp_start = None
    status_time_end = None
    status_time_start = None
    sel_counter = None
    progress = None
    apply_action = None
    remove_action = None
    filename_change_errors = list()
    filter_proxy = None

    def __init__(self):
        super().__init__()
        self.initUI()

    def exif_store_exception(self, error: OSError):
        self.filename_change_errors.append(error)

    def exif_store_filename_changed(self, idx: QModelIndex, new_filename: str, new_timedate: QDateTime):
        self.list_view_update_item_data(idx, {UserRolePicture.FileName: new_filename,
                                              UserRolePicture.TimeStamp: new_timedate,
                                              Qt.DisplayRole: new_timedate.toString(self.DATATIME_FORMAT)})

    def exif_store_errors(self, is_running: bool):
        if not is_running:
            if bool(self.filename_change_errors):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error")
                msg.setText("There was a problem with filename change.")
                msg.setInformativeText("Cannot change the file names.")
                errors_message = msg.setDetailedText("\n\n".join([str(item) for item in self.filename_change_errors]))
                msg.setDetailedText(errors_message)
                msg.exec_()
                del self.filename_change_errors[:]
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Update finished")
                msg.setText("All images were updated with success.")
                msg.exec_()

    def camera_view_add_item(self, camera: str, is_gps: bool):
        model: QAbstractItemModel = self.camera_view.model()
        first_idx = self.list_view.model().index(0, 0)
        idxes = model.match(first_idx, Qt.DisplayRole, camera, -1, Qt.MatchStartsWith)
        if bool(idxes):
            idx = idxes[0]
        else:
            # create a new row
            row_count = model.rowCount()
            model.insertRow(row_count)
            idx = model.index(row_count, 0)
            model.setData(idx, camera, Qt.DisplayRole)
        if is_gps:
            model.setData(idx, QIcon(get_icon("icons8-gps.png")), Qt.DecorationRole)

    def list_view_add_items(self, files: List[str]):
        # disable filtering
        self.camera_view.blockSignals(True)
        for row_idx in range(0, self.camera_view.model().rowCount()):
            idx = self.camera_view.model().index(row_idx, 0)
            if idx.data(Qt.CheckStateRole) == Qt.Unchecked:
                idx.model().setData(idx, Qt.Checked, Qt.CheckStateRole)
        self.camera_view.blockSignals(False)
        self.filter_proxy.setFilterRegExp("")
        self.list_view.model().sort(0)

        # insert rows
        model: QAbstractItemModel = self.list_view.model()
        row_start = model.rowCount()
        rows_count = len(files)
        if model.insertRows(row_start, rows_count):
            for id_loop, file in enumerate(files):
                file = os.path.normpath(file)
                idx = model.index(row_start + id_loop, 0)
                model.setData(idx, file, UserRolePicture.FileName)
                self.exif_loader_thread.load_item(QPersistentModelIndex(idx))
            self.exif_loader_thread.start(QThread.LowPriority)

    def list_view_update_item_data(self, persistent_idx: QPersistentModelIndex, data: Dict[int, QVariant]):
        if persistent_idx.isValid():
            idx = persistent_idx.model().index(persistent_idx.row(), persistent_idx.column())
            idx.model().setItemData(idx, data)
        else:
            print("Persistent model is not valid, cannot update element")

    def list_view_remove_item(self, persistent_idx: QPersistentModelIndex):
        if persistent_idx.isValid():
            persistent_idx.model().removeRow(persistent_idx.row())

    def camera_view_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        selection_model: QItemSelectionModel = self.list_view.selectionModel()
        # selection_model.clear()

        new_selection = QItemSelection()
        # Enable selected elements
        for sel_cam_idx in self.camera_view.selectedIndexes():
            first_idx = self.list_view.model().index(0, 0)
            camera_name = QVariant(sel_cam_idx.data())
            pic_items = self.list_view.model().match(first_idx, UserRolePicture.CameraModel, camera_name, -1,
                                                     Qt.MatchStartsWith)
            [new_selection.append(QItemSelectionRange(idx)) for idx in pic_items]
        selection_model.select(new_selection, QItemSelectionModel.ClearAndSelect)
        self.list_view_scroll_to_top()

    def list_view_scroll_to_top(self):
        items: List[QModelIndex] = self.list_view.selectedIndexes()
        if bool(items):
            items.sort(key=lambda idx: idx.data(UserRolePicture.TimeStamp), reverse=False)
            self.list_view.scrollTo(items[0], QAbstractItemView.PositionAtCenter)

    def list_view_scroll_to_bottom(self):
        items: List[QModelIndex] = self.list_view.selectedIndexes()
        if bool(items):
            items.sort(key=lambda idx: idx.data(UserRolePicture.TimeStamp), reverse=False)
            self.list_view.scrollTo(items[-1], QAbstractItemView.PositionAtCenter)

    def update_timerange(self):
        items: List[QModelIndex] = self.list_view.selectedIndexes()
        if bool(items):
            items.sort(key=lambda idx: idx.data(UserRolePicture.TimeStamp), reverse=False)
            self.sel_timestamp_start.blockSignals(True)
            self.sel_timestamp_start.setDateTime(items[0].data(UserRolePicture.TimeStamp))
            self.sel_timestamp_prev = self.sel_timestamp_start.dateTime()
            self.sel_timestamp_start.blockSignals(False)
            self.status_time_start.setDateTime(self.sel_timestamp_start.dateTime())
            self.status_time_end.setDateTime(items[-1].data(UserRolePicture.TimeStamp))

    def update_timestamps(self, datetime: QDateTime):
        timeshift_sec = self.sel_timestamp_prev.secsTo(datetime)

        # get selected items
        items: List[QModelIndex] = self.list_view.selectedIndexes()

        # shift all selected items by timeshift_sec
        for item in items:
            date = item.data(UserRolePicture.TimeStamp)
            if date.isValid():
                date = date.addSecs(timeshift_sec)
            else:
                # if item has no valid date then just set the start datetime
                date = datetime
            self.list_view.model().setData(item, date, UserRolePicture.TimeStamp)
            self.list_view.model().setData(item, date.toString(self.DATATIME_FORMAT), Qt.DisplayRole)

        self.update_timerange()
        self.list_view.model().sort(0)

    def apply_button_pressed(self):
        option_dialog = ApplyOptionDialog(self)
        if option_dialog.exec() == QDialog.Accepted:
            for row_idx in range(0, self.list_view.model().rowCount()):
                idx = self.list_view.model().index(row_idx, 0)
                timestamp = self.list_view.model().data(idx, UserRolePicture.TimeStamp)
                if timestamp.isValid():
                    filename = self.list_view.model().data(idx, UserRolePicture.FileName)
                    self.exif_store_thread.append_data((QPersistentModelIndex(idx), filename, timestamp))
            self.exif_store_thread.set_options(option_dialog.get_options())
            self.exif_store_thread.start()

    def remove_button_pressed(self):
        remove_dialog = RemoveConfirmationDialog(self)
        if remove_dialog.exec() == QDialog.Accepted:
            persistent_idx = [QPersistentModelIndex(idx) for idx in self.list_view.selectedIndexes()]
            self.remove_files_thread.set_elements_to_remove(persistent_idx)
            self.remove_files_thread.set_remove_from_disk(remove_dialog.is_remove_from_disk())
            self.remove_files_thread.start()

    def full_image_thread_starter(self):
        self.progress.setVisible(True)
        self.statusBar().showMessage("Loading full images...")

    def full_image_thread_finished(self):
        self.progress.setVisible(False)
        self.statusBar().clearMessage()

    def exif_store_thread_starter(self):
        self.apply_action.setEnabled(False)
        self.progress.setVisible(True)
        self.statusBar().showMessage("Saving exif data...")

    def exif_store_thread_finished(self):
        self.list_view.model().sort(0)
        self.apply_action.setEnabled(True)
        self.progress.setVisible(False)
        self.statusBar().clearMessage()

    def exif_loader_thread_starter(self):
        self.apply_action.setEnabled(False)
        self.progress.setVisible(True)
        self.statusBar().showMessage("Loading exif data...")

    def exif_loader_thread_finished(self):
        self.apply_action.setEnabled(True)
        self.statusBar().clearMessage()
        self.progress.setVisible(False)
        self.list_view.model().sort(0)
        self.list_view.model().persistentIndexList()
        for row_idx in range(0, self.list_view.model().rowCount()):
            idx = self.list_view.model().index(row_idx, 0)
            self.camera_view_add_item(idx.data(UserRolePicture.CameraModel),
                                      idx.data(UserRolePicture.IsGPS))
            if not idx.data(UserRolePicture.IsThumbnail):
                self.full_image_loader_thread.add_image(QPersistentModelIndex(idx))
        self.camera_view.model().sort(0)
        self.full_image_loader_thread.start(QThread.LowPriority)

    def remove_file_thread_starter(self):
        self.apply_action.setEnabled(False)
        self.remove_action.setEnabled(False)
        self.progress.setVisible(True)
        self.statusBar().showMessage("Deleting files ...")

    def remove_file_thread_finished(self):
        # update camera model
        for row_idx in reversed(range(0, self.camera_view.model().rowCount())):
            cam_idx = self.camera_view.model().index(row_idx, 0)
            camera_name = QVariant(cam_idx.data())
            first_idx = self.list_view.model().index(0, 0)
            pic_items = self.list_view.model().match(first_idx, UserRolePicture.CameraModel, camera_name, 1,
                                                     Qt.MatchExactly)
            if not pic_items:
                self.camera_view.model().removeRow(cam_idx.row())

        self.apply_action.setEnabled(True)
        self.statusBar().clearMessage()
        self.progress.setVisible(False)
        self.list_view.model().sort(0)
        self.list_view.model().persistentIndexList()

        exceptions = self.remove_files_thread.get_exception_log()
        if exceptions:
            msg = QMessageBox()
            msg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Exception")
            msg.setText("There was a problem with file(s) removing.")
            msg.setDetailedText("\n\n".join([str(item) for item in exceptions]))
            if len(exceptions) > 1:
                msg.setInformativeText("There were many errors, see details.")
            msg.exec_()

    def list_view_selection_changed(self, selection: QItemSelection, deselected: QItemSelection):
        selected_elements = self.list_view.selectedIndexes()
        self.sel_counter.setText(str(len(selected_elements)))
        self.update_timerange()
        self.remove_action.setEnabled(bool(selected_elements))

    def list_view_update_tooltip(self, top_left: QModelIndex, bottom_right: QModelIndex, roles):
        roles_as_set = set(roles)
        tooltip_roles = {UserRolePicture.FileName, UserRolePicture.CameraModel}
        if bool(roles_as_set.intersection(tooltip_roles)):
            for idx in QItemSelection(top_left, bottom_right).indexes():
                timestamp = idx.data(UserRolePicture.TimeStamp)
                if not timestamp:
                    timestamp = QDateTime()
                file = idx.data(UserRolePicture.FileName)
                if not file:
                    file = ""
                camera = idx.data(UserRolePicture.CameraModel)
                if not camera:
                    camera = "Unknown"
                tooltip = "Original time: {0}<br>File: {1}<br>Camera: {2}".format(
                    timestamp.toString(self.DATATIME_FORMAT), os.path.basename(file), camera)
                idx.model().setData(idx, tooltip, Qt.ToolTipRole)

    def camera_item_data_changed(self, top_left: QModelIndex, bottom_right: QModelIndex, roles):
        if Qt.CheckStateRole in roles:
            camera_model = top_left.model()
            selected_cameras = set()
            for row_idx in range(0, camera_model.rowCount()):
                idx = camera_model.index(row_idx, 0)
                if camera_model.data(idx, Qt.CheckStateRole) == Qt.Checked:
                    selected_cameras.add(camera_model.data(idx, Qt.DisplayRole))

            regex = "|".join(selected_cameras)
            if not regex:
                regex = "--------"
            self.filter_proxy.setFilterRegExp(regex)
            self.list_view.model().sort(0)

    def action_add_files(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select images", "", "JPG (*.jpg)", options=options)
        self.list_view_add_items(files)

    def initUI_status_bar(self):
        self.sel_counter = QLabel("0")

        selection_layout = QHBoxLayout()
        selection_layout.addWidget(QLabel("Selected: "))
        selection_layout.addWidget(self.sel_counter)

        selection_widget = QWidget()
        selection_widget.setLayout(selection_layout)

        self.status_time_start = QDateTimeEdit()
        self.status_time_start.setFrame(False)
        self.status_time_start.setReadOnly(True)
        self.status_time_start.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.status_time_start.setDisplayFormat(self.DATATIME_FORMAT)
        self.sel_timestamp_start.dateTimeChanged.connect(self.status_time_start.setDateTime)

        self.status_time_end = QDateTimeEdit()
        self.status_time_end.setFrame(False)
        self.status_time_end.setReadOnly(True)
        self.status_time_end.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.status_time_end.setDisplayFormat(self.DATATIME_FORMAT)

        range_layout = QHBoxLayout()
        range_layout.addWidget(QLabel("Time range: "))
        range_layout.addWidget(self.status_time_start)
        range_layout.addWidget(self.status_time_end)

        range_widget = QWidget()
        range_widget.setLayout(range_layout)

        self.statusBar().addPermanentWidget(selection_widget)
        self.statusBar().addPermanentWidget(range_widget)

    def initUI_tool_bar(self):
        tb: QToolBar = QToolBar("Actions")
        tb.addAction(QIcon(get_icon("icons8-add-file.png")), "Add more files . . .", self.action_add_files)
        self.remove_action = tb.addAction(QIcon(get_icon("icons8-delete-file.png")),
                                          "Remove files . . .", self.remove_button_pressed)
        tb.addSeparator()
        tb.addAction(QIcon(get_icon("icons8-up.png")), "Jump to first selected image",
                     self.list_view_scroll_to_top)
        tb.addAction(QIcon(get_icon("icons8-down.png")), "Jump to last selected image",
                     self.list_view_scroll_to_bottom)
        tb.addSeparator()
        self.apply_action = tb.addAction(QIcon(get_icon("icons8-save.png")),
                                         "Apply changes . . .", self.apply_button_pressed)
        self.remove_action.setEnabled(False)
        self.addToolBar(Qt.RightToolBarArea, tb)

    def initUI(self):

        self.sel_timestamp_start = QDateTimeEdit()
        self.sel_timestamp_start.setFrame(True)
        self.sel_timestamp_start.setReadOnly(False)
        self.sel_timestamp_start.setDisplayFormat(self.DATATIME_FORMAT)
        self.sel_timestamp_start.dateTimeChanged.connect(self.update_timestamps)
        self.sel_timestamp_start.setObjectName("timeShifter")

        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(15)
        form_layout.addRow("First image:", self.sel_timestamp_start)

        item_prototype = QStandardItem(QIcon(get_icon("icons8-loader.png")), "Loading in progress")
        item_prototype.setEditable(False)
        item_prototype.setSelectable(True)
        item_prototype.setCheckable(False)
        item_prototype.setSizeHint(QSize(256, 256))
        model = QStandardItemModel(self)
        model.setItemPrototype(item_prototype)
        model.insertColumn(0)
        model.setSortRole(UserRolePicture.TimeStamp)

        self.filter_proxy = QSortFilterProxyModel()
        self.filter_proxy.setDynamicSortFilter(False)
        self.filter_proxy.setSourceModel(model)
        self.filter_proxy.setFilterRole(UserRolePicture.CameraModel)
        self.filter_proxy.setSortRole(UserRolePicture.TimeStamp)

        self.list_view = QListView()
        self.list_view.setModel(self.filter_proxy)
        self.list_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list_view.setViewMode(QListView.IconMode)
        self.list_view.setWrapping(True)
        self.list_view.setFlow(QListView.LeftToRight)
        self.list_view.setIconSize(QSize(256, 256))
        self.list_view.setUniformItemSizes(True)
        self.list_view.setResizeMode(QListView.Adjust)
        self.list_view.selectionModel().selectionChanged.connect(self.list_view_selection_changed)
        self.list_view.model().dataChanged.connect(self.list_view_update_tooltip)
        self.list_view.setDragEnabled(False)
        self.list_view.setAcceptDrops(False)
        self.list_view.setGridSize(QSize(276, 326))

        camera_item_prototype = QStandardItem()
        camera_item_prototype.setEditable(False)
        camera_item_prototype.setTristate(False)
        camera_item_prototype.setCheckable(True)
        camera_item_prototype.setCheckState(Qt.Checked)

        cameras_model = QStandardItemModel(self)
        cameras_model.insertColumn(0)
        cameras_model.setItemPrototype(camera_item_prototype)
        cameras_model.setSortRole(Qt.DisplayRole)
        cameras_model.dataChanged.connect(self.camera_item_data_changed)
        self.camera_view = QListView()
        self.camera_view.setModel(cameras_model)
        self.camera_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.camera_view.setViewMode(QListView.ListMode)
        self.camera_view.setResizeMode(QListView.Adjust)
        self.camera_view.setMinimumHeight(500)
        camera_selection_model: QItemSelectionModel = self.camera_view.selectionModel()
        camera_selection_model.selectionChanged.connect(self.camera_view_selection_changed)
        form_layout.addRow("Camera:", self.camera_view)

        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setMaximumHeight(8)

        list_proggress_layout = QVBoxLayout()
        list_proggress_layout.addWidget(self.list_view)
        list_proggress_layout.addWidget(self.progress)
        list_proggress_layout.setSpacing(0)

        # Scroll Area Layer add
        main_layout = QHBoxLayout()
        main_layout.addLayout(list_proggress_layout, 2)
        main_layout.addSpacing(20)
        main_layout.addLayout(form_layout)

        self.exif_store_thread.progress_changed.connect(self.progress.setValue)
        self.exif_store_thread.progress_max_changed.connect(self.progress.setMaximum)
        self.exif_store_thread.started.connect(self.exif_store_thread_starter)
        self.exif_store_thread.finished.connect(self.exif_store_thread_finished)
        self.exif_store_thread.filename_changed.connect(self.exif_store_filename_changed)
        self.exif_store_thread.is_running.connect(self.exif_store_errors)
        self.exif_store_thread.exception.connect(self.exif_store_exception)

        self.exif_loader_thread.loaded.connect(self.list_view_update_item_data, Qt.QueuedConnection)
        self.exif_loader_thread.progress_changed.connect(self.progress.setValue)
        self.exif_loader_thread.progress_max_changed.connect(self.progress.setMaximum)
        self.exif_loader_thread.started.connect(self.exif_loader_thread_starter)
        self.exif_loader_thread.finished.connect(self.exif_loader_thread_finished)
        self.exif_loader_thread.set_timestamp_format(self.DATATIME_FORMAT)

        self.full_image_loader_thread.loaded.connect(self.list_view_update_item_data, Qt.QueuedConnection)
        self.full_image_loader_thread.progress_changed.connect(self.progress.setValue)
        self.full_image_loader_thread.progress_max_changed.connect(self.progress.setMaximum)
        self.full_image_loader_thread.started.connect(self.full_image_thread_starter)
        self.full_image_loader_thread.finished.connect(self.full_image_thread_finished)

        self.remove_files_thread.removed.connect(self.list_view_remove_item, Qt.QueuedConnection)
        self.remove_files_thread.progress_changed.connect(self.progress.setValue)
        self.remove_files_thread.progress_max_changed.connect(self.progress.setMaximum)
        self.remove_files_thread.started.connect(self.remove_file_thread_starter)
        self.remove_files_thread.finished.connect(self.remove_file_thread_finished)

        # self.setLayout(main_layout)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.initUI_status_bar()
        self.initUI_tool_bar()

        self.action_add_files()

        self.setGeometry(200, 100, 1600, 800)
        self.showMaximized()
        self.setWindowTitle('JPG Sorter')
        self.show()


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("* { Font: 20px; } \
    QDateTimeEdit#timeShifter {width: 220px; height: 50px;} \
    QStatusBar QDateTimeEdit {background: transparent;} \
    QPushButton {height: 50px;} \
    QToolBar {icon-size: 64px;} \
    QListView::item:selected {background: DeepSkyBlue;}")
    app.setWindowIcon(QIcon(get_icon("icons8-time-machine.png")))
    ex = JpgSorter()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
