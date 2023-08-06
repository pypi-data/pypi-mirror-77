import pkg_resources
import time

from PyQt5 import uic, QtCore, QtWidgets

from ...upload import UploadJobList
from ...settings import SettingsFile

from .dlg_upload import UploadDialog


class UploadWidget(QtWidgets.QWidget):
    upload_finished = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        """Manage running uploads
        """
        super(UploadWidget, self).__init__(*args, **kwargs)
        path_ui = pkg_resources.resource_filename(
            "dcoraid.gui.upload", "widget_upload.ui")
        uic.loadUi(path_ui, self)

        self.toolButton_new_upload.clicked.connect(self.on_draft_upload)
        self._upload_dialogs = []

        # Underlying upload class
        settings = SettingsFile()
        self.jobs = UploadJobList(server=settings.get_string("server"),
                                  api_key=settings.get_string("api key"))
        self.widget_jobs.set_job_list(self.jobs)

        # upload finished signal
        self.widget_jobs.upload_finished.connect(self.upload_finished)

    @QtCore.pyqtSlot()
    def on_draft_upload(self):
        dlg = UploadDialog(self)
        dlg.finished.connect(self.on_run_upload)
        self._upload_dialogs.append(dlg)
        dlg.show()

    @QtCore.pyqtSlot(object)
    def on_run_upload(self, upload_dialog):
        files = upload_dialog.get_file_list()
        dataset_dict = upload_dialog.dataset_dict
        # add the entry to the job list
        self.jobs.add_job(dataset_dict, files)


class UploadTableWidget(QtWidgets.QTableWidget):
    upload_finished = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(UploadTableWidget, self).__init__(*args, **kwargs)
        self.jobs = []  # Will become UploadJobList with self.set_job_list
        self.watcher = UpdateTriggerer()
        self.watcher.trigger.connect(self.update_job_status)
        self.watcher.start()
        self._finished_uploads = []

    def set_job_list(self, jobs):
        """Set the current job list

        The job list can be a `list`, but it is actually
        an `UploadJobList`.
        """
        # This is the actual initialization
        self.jobs = jobs

    def on_upload_finished(self, dataset_id):
        """Triggers upload_finished whenever an upload is finished"""
        if dataset_id not in self._finished_uploads:
            self._finished_uploads.append(dataset_id)
            self.upload_finished.emit()

    @QtCore.pyqtSlot()
    def update_job_status(self):
        """Update UI with information from self.jobs (UploadJobList)"""
        # make sure the length of the table is long enough
        # disable updates
        self.setUpdatesEnabled(False)
        # rows'n'cols
        self.setRowCount(len(self.jobs))
        self.setColumnCount(6)

        for row, job in enumerate(self.jobs):
            status = job.get_status()
            self.set_label_item(row, 0, job.dataset_id[:5])
            self.set_label_item(row, 1, job.dataset_dict["title"])
            self.set_label_item(row, 2, status["state"])
            plural = "s" if status["files total"] > 1 else ""
            if status["state"] == "running":
                progress = "{:.0f}% (file {}/{})".format(
                    status["bytes uploaded"]/status["bytes total"]*100,
                    status["files uploaded"]+1,
                    status["files total"])
            elif status["state"] in ["finished", "finalizing"]:
                progress = "100% ({} file{})".format(status["files total"],
                                                     plural)
                if status["state"] == "finished":
                    self.on_upload_finished(job.dataset_id)
            elif status["state"] == "queued":
                progress = "0% (0/{} file{})".format(status["files total"],
                                                     plural)
            self.set_label_item(row, 3, progress)
            rate = status["rate"]
            if rate > 1e6:
                rate_label = "{:.1f} MB/s".format(rate/1e6)
            else:
                rate_label = "{:.0f} kB/s".format(rate/1e3)
            self.set_label_item(row, 4, rate_label)

        # spacing (did not work in __init__)
        header = self.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        # enable updates again
        self.setUpdatesEnabled(True)

    def set_label_item(self, row, col, label):
        """Get/Create a Qlabel at the specified position

        User has to make sure that row and column count are set
        """
        label = "{}".format(label)
        item = self.item(row, col)
        if item is None:
            item = QtWidgets.QTableWidgetItem(label)
            item .setFlags(QtCore.Qt.ItemIsEnabled)
            self.setItem(row, col, item)
        else:
            if item.text() != label:
                item.setText(label)


class UpdateTriggerer(QtCore.QThread):
    trigger = QtCore.pyqtSignal()

    def run(self):
        while True:
            self.trigger.emit()
            time.sleep(1/30)
