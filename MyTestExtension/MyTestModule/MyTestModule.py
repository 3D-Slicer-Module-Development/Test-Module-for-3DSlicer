import os
import unittest
import logging
import SegmentStatistics
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin


#
# Filename should be same as the classname
# This class is to declare some important information of this module
class MyTestModule:
    def __init__(self, parent):
        parent.title = "Test Module"
        parent.categories = ["Test Extension 1"]
        parent.dependencies = []
        parent.contributors = ["Someone"]
        parent.helpText = """ 
    Display the correct path to a loaded volume.
    """
        parent.acknowledgementText = """
      # replace with the organization, grant and thanks
    """
        self.parent = parent




class MyTestModuleWidget:
    def __init__(self, parent=None):
        if not parent:
            self.parent = slicer.qHRMLWidget()
            self.parent.setLayout(qt.QVBoxLayout())
            self.parent.setMRMLScene(slicer.mrmlScene)
        else:
            self.parent = parent
        self.layout = self.parent.layout()
        if not parent:
            self.setup()
            self.parent.show()



    def setup(self):
        # create collapsible button
        collapsibleButton = ctk.ctkCollapsibleButton()
        collapsibleButton.text = "My collapsible Menu"


        # bind collapsible button to root layout
        # 将可折叠按钮绑定到根布局
        self.layout.addWidget(collapsibleButton)

        # new layout for collapsible button
        self.formLayout = qt.QFormLayout(collapsibleButton)



        self.formFrame = qt.QFrame(collapsibleButton)

        # set the layout to horizontal
        self.formFrame.setLayout(qt.QHBoxLayout())

        # Bind this formFrame to an existing layout
        self.formLayout.addWidget(self.formFrame)

        # volume selector
        # create new volume selector, the label of this selector
        self.inputSelector = qt.QLabel("Input Volume: ", self.formFrame)
        self.formFrame.layout().addWidget(self.inputSelector)

        self.inputSelector = slicer.qMRMLNodeComboBox(self.formFrame)


        # Declare what type of node the combobox selects, here is volume: vtkMRMLScalarVolumeNode
        # self.inputSelector.nodeTypes = (("vtkMRMLSegmentationNode"), "")
        self.inputSelector.nodeTypes = (("vtkMRMLScalarVolumeNode"), "")
        self.inputSelector.addEnabled = False
        self.inputSelector.removeEnabled = False
        # Bind the current volume selector combobox to the current scene of the slicer
        self.inputSelector.setMRMLScene(slicer.mrmlScene)

        # Bind the combobox to formFrame
        self.formFrame.layout().addWidget(self.inputSelector)




        # A button
        # Tooltip is the help information seen by hovering the mouse
        button = qt.QPushButton("Get volume value")
        button.toolTip = "Displays the volume value of the selected volume"

        # When the button is clicked, the function defined below is executed to complete the function
        # 点击按钮触发要执行的函数以完成功能
        button.connect("clicked(bool)", self.informationButtonClicked)
        # Bind button to frame
        self.formFrame.layout().addWidget(button)

        # A textfield
        # self.textfield = qt.QTextEdit()
        # self.textfield.setReadOnly(True)
        # # Bind textfield to frame
        # self.formFrame.layout().addWidget(self.textfield)


    # All actions performed when the button is clicked
    def informationButtonClicked(self):

        # Set the current node as the masterVolumeNode for surface extraction
        masterVolumeNode = slicer.util.getNode(self.inputSelector.currentNode().GetName())

        # Create segmentation
        segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
        segmentationNode.CreateDefaultDisplayNodes()  # only needed for display
        segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)
        addedSegmentID = segmentationNode.GetSegmentation().AddEmptySegment("Extracted surface")
        
        # Create segment editor to get access to effects
        segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
        segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
        segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
        segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
        segmentEditorWidget.setSegmentationNode(segmentationNode)
        segmentEditorWidget.setMasterVolumeNode(masterVolumeNode)

        # Thresholding  结合阈值化模块(操作)就不需要了
        # TODO: Thresholding through the slider
        segmentEditorWidget.setActiveEffectByName("Threshold")
        # effect = segmentEditorgetNodeWidget.activeEffect()
        effect = segmentEditorWidget.activeEffect()
        #effect.setParameter("MinimumThreshold", "100")
        #effect.setParameter("MaximumThreshold", "3522")
        effect.self().onApply()

        # Calculate the volume of the extracted surface by using the method in the SegmentStatistics module
        # TODO: Extract and calculate the volume value of all intersections
        segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
        segStatLogic.getParameterNode().SetParameter("Segmentation", segmentationNode.GetID())
        segStatLogic.computeStatistics()
        stats = segStatLogic.getStatistics()

        # Display volume of each segment
        for segmentId in stats["SegmentIDs"]:
            volume_cm3 = stats[segmentId, "LabelmapSegmentStatisticsPlugin.volume_cm3"]
            # segmentName = segmentationNode.GetSegmentation().GetSegment(segmentId).GetName()
            VolumeName =  masterVolumeNode.GetName()
            Result = 'The volume of {name} is {volumevalue} cm3'
            FinalResult = Result.format(name = VolumeName, volumevalue = round(volume_cm3,3))
            #self.textfield.insertPlainText(FinalResult + '\n')

            # Export results to a table
            resultsTableNode = slicer.vtkMRMLTableNode()
            slicer.mrmlScene.AddNode(resultsTableNode)
            segStatLogic.exportToTable(resultsTableNode)
            t = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLTableNode")
            t.RemoveColumn(1)
            segStatLogic.showTable(resultsTableNode)
            













