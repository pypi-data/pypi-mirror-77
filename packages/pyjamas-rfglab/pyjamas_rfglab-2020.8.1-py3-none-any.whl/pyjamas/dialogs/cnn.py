"""
    PyJAMAS is Just A More Awesome Siesta
    Copyright (C) 2018  Rodrigo Fernandez-Gonzalez (rodrigo.fernandez.gonzalez@utoronto.ca)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from PyQt5 import QtCore, QtWidgets

from pyjamas.dialogs.classifierdialogABC import ClassifierDialogABC
import pyjamas.rimage.rimclassifier.rimnn as rimnn
from pyjamas.rutils import RUtils


class LeNetDialog(ClassifierDialogABC):
    epochs: int = rimnn.LeNet.EPOCHS
    learning_rate: float = rimnn.LeNet.LEARNING_RATE
    mini_batch_size = rimnn.LeNet.MINI_BATCH_SIZE

    def __init__(self):
        super().__init__()

    def setupUi(self, CNN, parameters: dict = None):
        if parameters is None or parameters is False:
            parameters = {
                'positive_training_folder': LeNetDialog.positive_training_folder,
                'negative_training_folder': LeNetDialog.negative_training_folder,
                'hard_negative_training_folder': LeNetDialog.hard_negative_training_folder,
                'train_image_size': LeNetDialog.train_image_size,
                'step_sz': LeNetDialog.step_sz,
                'epochs': LeNetDialog.epochs,
                'learning_rate': LeNetDialog.learning_rate,
                'mini_batch_size': LeNetDialog.mini_batch_size,
            }

        LeNetDialog.positive_training_folder = parameters.get('positive_training_folder', LeNetDialog.positive_training_folder)
        LeNetDialog.negative_training_folder = parameters.get('negative_training_folder', LeNetDialog.negative_training_folder)
        LeNetDialog.hard_negative_training_folder = parameters.get('hard_negative_training_folder', LeNetDialog.hard_negative_training_folder)
        LeNetDialog.histogram_of_gradients = parameters.get('histogram_of_gradients', LeNetDialog.histogram_of_gradients)
        LeNetDialog.train_image_size = parameters.get('train_image_size', LeNetDialog.train_image_size)
        LeNetDialog.step_sz = parameters.get('step_sz', LeNetDialog.step_sz)
        LeNetDialog.epochs = parameters.get('epochs', LeNetDialog.epochs)
        LeNetDialog.learning_rate = parameters.get('learning_rate', LeNetDialog.learning_rate)
        LeNetDialog.mini_batch_size = parameters.get('mini_batch_size', LeNetDialog.mini_batch_size)

        CNN.setObjectName("CNN")
        CNN.resize(614, 340)
        self.buttonBox = QtWidgets.QDialogButtonBox(CNN)
        self.buttonBox.setGeometry(QtCore.QRect(240, 290, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox_2 = QtWidgets.QGroupBox(CNN)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 26, 551, 121))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(31, 26, 141, 24))
        self.label.setObjectName("label")
        self.positive_training_folder_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.positive_training_folder_edit.setGeometry(QtCore.QRect(220, 30, 261, 21))
        self.positive_training_folder_edit.setObjectName("positive_training_folder_edit")
        self.positive_training_folder_edit.setText(LeNetDialog.positive_training_folder)
        self.btnSavePositive = QtWidgets.QToolButton(self.groupBox_2)
        self.btnSavePositive.setGeometry(QtCore.QRect(490, 30, 26, 22))
        self.btnSavePositive.setObjectName("btnSavePositive")
        self.btnSavePositive.clicked.connect(self._open_positive_folder_dialog)
        self.negative_training_folder_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.negative_training_folder_edit.setGeometry(QtCore.QRect(220, 60, 261, 21))
        self.negative_training_folder_edit.setObjectName("negative_training_folder_edit")
        self.negative_training_folder_edit.setText(LeNetDialog.negative_training_folder)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(31, 56, 141, 24))
        self.label_2.setObjectName("label_2")
        self.btnSaveNegative = QtWidgets.QToolButton(self.groupBox_2)
        self.btnSaveNegative.setGeometry(QtCore.QRect(490, 60, 26, 22))
        self.btnSaveNegative.setObjectName("btnSaveNegative")
        self.btnSaveNegative.clicked.connect(self._open_negative_folder_dialog)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(31, 86, 181, 24))
        self.label_3.setObjectName("label_3")
        self.btnSaveHard = QtWidgets.QToolButton(self.groupBox_2)
        self.btnSaveHard.setGeometry(QtCore.QRect(490, 90, 26, 22))
        self.btnSaveHard.setObjectName("btnSaveHard")
        self.btnSaveHard.clicked.connect(self._open_hard_folder_dialog)
        self.hard_negative_training_folder_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.hard_negative_training_folder_edit.setGeometry(QtCore.QRect(220, 90, 261, 21))
        self.hard_negative_training_folder_edit.setObjectName("hard_negative_training_folder_edit")
        self.hard_negative_training_folder_edit.setText(LeNetDialog.hard_negative_training_folder)
        self.groupBox_3 = QtWidgets.QGroupBox(CNN)
        self.groupBox_3.setGeometry(QtCore.QRect(30, 156, 251, 61))
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setGeometry(QtCore.QRect(31, 28, 141, 24))
        self.label_4.setObjectName("label_4")
        self.lnWidth = QtWidgets.QLineEdit(self.groupBox_3)
        self.lnWidth.setGeometry(QtCore.QRect(70, 30, 31, 21))
        self.lnWidth.setObjectName("lnWidth")
        self.lnWidth.setText(str(LeNetDialog.train_image_size[1]))
        self.lnHeight = QtWidgets.QLineEdit(self.groupBox_3)
        self.lnHeight.setGeometry(QtCore.QRect(170, 30, 31, 21))
        self.lnHeight.setObjectName("lnHeight")
        self.lnHeight.setText(str(LeNetDialog.train_image_size[0]))
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(120, 28, 141, 24))
        self.label_5.setObjectName("label_5")
        self.label_5.raise_()
        self.label_4.raise_()
        self.lnWidth.raise_()
        self.lnHeight.raise_()
        self.groupBox_5 = QtWidgets.QGroupBox(CNN)
        self.groupBox_5.setGeometry(QtCore.QRect(30, 226, 551, 60))
        self.groupBox_5.setObjectName("groupBox_5")
        self.lnEpochs = QtWidgets.QLineEdit(self.groupBox_5)
        self.lnEpochs.setGeometry(QtCore.QRect(470, 27, 41, 21))
        self.lnEpochs.setObjectName("lnEpochs")
        self.lnEpochs.setText(str(LeNetDialog.epochs))
        self.label_10 = QtWidgets.QLabel(self.groupBox_5)
        self.label_10.setGeometry(QtCore.QRect(380, 31, 91, 16))
        self.label_10.setObjectName("label_10")
        self.lnEta = QtWidgets.QLineEdit(self.groupBox_5)
        self.lnEta.setGeometry(QtCore.QRect(120, 27, 46, 21))
        self.lnEta.setObjectName("lnEta")
        self.lnEta.setText(str(LeNetDialog.learning_rate))
        self.label_11 = QtWidgets.QLabel(self.groupBox_5)
        self.label_11.setGeometry(QtCore.QRect(34, 31, 141, 16))
        self.label_11.setObjectName("label_11")
        self.lnBatchSz = QtWidgets.QLineEdit(self.groupBox_5)
        self.lnBatchSz.setGeometry(QtCore.QRect(305, 27, 36, 21))
        self.lnBatchSz.setObjectName("lnBatchSz")
        self.lnBatchSz.setText(str(LeNetDialog.mini_batch_size))
        self.label_14 = QtWidgets.QLabel(self.groupBox_5)
        self.label_14.setGeometry(QtCore.QRect(205, 31, 95, 16))
        self.label_14.setObjectName("label_14")
        self.label_10.raise_()
        self.lnEpochs.raise_()
        self.label_11.raise_()
        self.lnEta.raise_()
        self.label_14.raise_()
        self.lnBatchSz.raise_()
        self.groupBox_6 = QtWidgets.QGroupBox(CNN)
        self.groupBox_6.setGeometry(QtCore.QRect(300, 155, 281, 61))
        self.groupBox_6.setObjectName("groupBox_6")
        self.label_12 = QtWidgets.QLabel(self.groupBox_6)
        self.label_12.setGeometry(QtCore.QRect(31, 28, 141, 24))
        self.label_12.setObjectName("label_12")
        self.lnRow = QtWidgets.QLineEdit(self.groupBox_6)
        self.lnRow.setGeometry(QtCore.QRect(70, 30, 31, 21))
        self.lnRow.setObjectName("lnRow")
        self.lnRow.setText(str(LeNetDialog.step_sz[0]))
        self.lnColumn = QtWidgets.QLineEdit(self.groupBox_6)
        self.lnColumn.setGeometry(QtCore.QRect(180, 30, 31, 21))
        self.lnColumn.setObjectName("lnColumn")
        self.lnColumn.setText(str(LeNetDialog.step_sz[1]))
        self.label_13 = QtWidgets.QLabel(self.groupBox_6)
        self.label_13.setGeometry(QtCore.QRect(120, 28, 141, 24))
        self.label_13.setObjectName("label_13")
        self.label_13.raise_()
        self.label_12.raise_()
        self.lnRow.raise_()
        self.lnColumn.raise_()

        self.retranslateUi(CNN)
        self.buttonBox.accepted.connect(CNN.accept)
        self.buttonBox.rejected.connect(CNN.reject)
        QtCore.QMetaObject.connectSlotsByName(CNN)

    def retranslateUi(self, CNN):
        _translate = QtCore.QCoreApplication.translate
        CNN.setWindowTitle(_translate("CNN", "Train LeNet network"))
        self.groupBox_2.setTitle(_translate("CNN", "Project files"))
        self.label.setText(_translate("CNN", "positive training folder"))
        self.btnSavePositive.setText(_translate("CNN", "..."))
        self.label_2.setText(_translate("CNN", "negative training folder"))
        self.btnSaveNegative.setText(_translate("CNN", "..."))
        self.label_3.setText(_translate("CNN", "hard negative training folder"))
        self.btnSaveHard.setText(_translate("CNN", "..."))
        self.groupBox_3.setTitle(_translate("CNN", "Training image size"))
        self.label_4.setText(_translate("CNN", "width"))
        self.label_5.setText(_translate("CNN", "height"))
        self.groupBox_5.setTitle(_translate("CNN", "LeNet parameters"))
        self.label_10.setText(_translate("CNN", "no. of epochs"))
        self.label_11.setText(_translate("CNN", "learning rate"))
        self.groupBox_6.setTitle(_translate("CNN", "Image step size"))
        self.label_12.setText(_translate("CNN", "rows"))
        self.label_13.setText(_translate("CNN", "columns"))
        self.label_14.setText(_translate("CNN", "mini-batch size"))

    def parameters(self) -> dict:
        LeNetDialog.positive_training_folder = self.positive_training_folder_edit.text()
        LeNetDialog.negative_training_folder = self.negative_training_folder_edit.text()
        LeNetDialog.hard_negative_training_folder = self.hard_negative_training_folder_edit.text()
        LeNetDialog.train_image_size = int(self.lnHeight.text()), int(self.lnWidth.text())
        LeNetDialog.step_sz = (int(self.lnRow.text()), int(self.lnColumn.text()))
        LeNetDialog.epochs = int(self.lnEpochs.text())
        LeNetDialog.learning_rate = float(self.lnEta.text())
        LeNetDialog.mini_batch_size = int(self.lnBatchSz.text())

        theparameters = {'positive_training_folder': LeNetDialog.positive_training_folder,
                         'negative_training_folder': LeNetDialog.negative_training_folder,
                         'hard_negative_training_folder': LeNetDialog.hard_negative_training_folder,
                         'train_image_size': LeNetDialog.train_image_size,
                         'step_sz': LeNetDialog.step_sz,
                         'epochs': LeNetDialog.epochs,
                         'learning_rate': LeNetDialog.learning_rate,
                         'mini_batch_size': LeNetDialog.mini_batch_size
                         }

        return theparameters
