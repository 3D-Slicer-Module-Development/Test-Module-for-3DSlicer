import logging
import os
import unittest
import vtk, qt, ctk, slicer
import SegmentStatistics
from slicer.ScriptedLoadableModule import *
from slicer.util import TESTING_DATA_URL



class ScriptedLoadableModuleTemplate(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Threshold Example" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Test Extension 2"]
    self.parent.dependencies = []
    self.parent.contributors = ["John Doe (AnyWare Corp.)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    The Help text for this scripted module.
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()

    self.parent.acknowledgementText = """
   The acknowledgementText
"""

#
# ScriptedLoadableModuleTemplateWidget
#

class ScriptedLoadableModuleTemplateWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...
    # 实例化和连接小部件

    #
    # Parameters Area  参数域
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    # 布局内的虚拟可折叠按钮  new layout for collapsible button
    # parametersFormLayout 相当于是 formLayout
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # input volume selector
    #
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Input Volume: ", self.inputSelector)

    #
    # thresholdRangeSlider
    #
    self.thresholdRangeSlider1 = ctk.ctkRangeWidget()
    self.thresholdRangeSlider1.minimum = 0.0
    self.thresholdRangeSlider1.maximum = 3522.0
    self.thresholdRangeSlider1.singleStep = 0.1

    self.thresholdRangeSlider1.minimumValue = 1.0
    self.thresholdRangeSlider1.maximumValue = 3522.0
    parametersFormLayout.addRow("Thresholds:", self.thresholdRangeSlider1)

    # check box to trigger taking screen shots for later use in tutorials
    # self.enableScreenshotsFlagCheckBox = qt.QCheckBox()
    # self.enableScreenshotsFlagCheckBox.checked = 0
    # self.enableScreenshotsFlagCheckBox.setToolTip("If checked, take screen shots for tutorials. Use Save Data to write them to disk.")
    # parametersFormLayout.addRow("Enable Screenshots", self.enableScreenshotsFlagCheckBox)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)


    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  def cleanup(self):
    pass

  def onSelect(self):
    # self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()
    self.applyButton.enabled = self.inputSelector.currentNode()

  def onApplyButton(self):
    logic = ScriptedLoadableModuleTemplateLogic()
    LowerimageThreshold2 = self.thresholdRangeSlider1.minimumValue
    UpperimageThreshold2 = self.thresholdRangeSlider1.maximumValue
    logic.run(self.inputSelector.currentNode(), LowerimageThreshold2, UpperimageThreshold2)

#
# ScriptedLoadableModuleTemplateLogic
#

class ScriptedLoadableModuleTemplateLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def run(self, inputVolume, LowerimageThreshold2, UpperimageThreshold2):
    """
    Run the actual algorithm
    执行实际的算法实现相应的功能
    """

    # if not self.isValidInputOutputData(inputVolume, outputVolume):
    #   slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
    #   return False
    logging.info('Processing started')

    # 阈值化分割操作  The Segmentation after thresholding
    # Compute the thresholded output volume using the Threshold Scalar Volume CLI module
    MyinputVolume = inputVolume.GetName()
    voxelArray = slicer.util.array(MyinputVolume)
    voxelArray[voxelArray < LowerimageThreshold2] = 0
    voxelArray[voxelArray > UpperimageThreshold2] = 0
    slicer.util.getNode(MyinputVolume).Modified()

    #Surface Extraction 表面提取
    masterVolumeNode = slicer.mrmlScene.GetNodeByID('vtkMRMLScalarVolumeNode1')

    # Create segmentation
    segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
    segmentationNode.CreateDefaultDisplayNodes()  # only needed for display
    segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)
    addedSegmentID = segmentationNode.GetSegmentation().AddEmptySegment("Tissue-red-channel")

    # Create segment editor to get access to effects
    segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
    segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
    segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
    segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
    segmentEditorWidget.setSegmentationNode(segmentationNode)
    segmentEditorWidget.setMasterVolumeNode(masterVolumeNode)

    segmentEditorWidget.setActiveEffectByName("Threshold")
    effect = segmentEditorWidget.activeEffect()
    MinimumThreshold1 = LowerimageThreshold2
    MaximumThreshold1 = UpperimageThreshold2
    effect.setParameter("MinimumThreshold", str(MinimumThreshold1))
    effect.setParameter("MaximumThreshold", str(MaximumThreshold1))

    effect.self().onApply()

    segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
    segStatLogic.getParameterNode().SetParameter("Segmentation", segmentationNode.GetID())
    segStatLogic.computeStatistics()
    stats = segStatLogic.getStatistics()

    # Display volume of each segment
    for segmentId in stats["SegmentIDs"]:
      volume_cm3 = stats[segmentId, "LabelmapSegmentStatisticsPlugin.volume_cm3"]
      # segmentName = segmentationNode.GetSegmentation().GetSegment(segmentId).GetName()
      VolumeName = masterVolumeNode.GetName()
      Result = 'The volume of {name} is {volumevalue} cm3'
      FinalResult = Result.format(name=VolumeName, volumevalue=round(volume_cm3, 3))
      # self.textfield.insertPlainText(FinalResult + '\n')

      # Export results to a table
      resultsTableNode = slicer.vtkMRMLTableNode()
      slicer.mrmlScene.AddNode(resultsTableNode)
      segStatLogic.exportToTable(resultsTableNode)
      t = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLTableNode")
      t.RemoveColumn(1)
      segStatLogic.showTable(resultsTableNode)



    # 更新体绘制效果
    # volRenLogic = slicer.modules.volumerendering.logic()
    # displayNode = volRenLogic.GetFirstVolumeRenderingDisplayNode(MyinputVolume)
    # volRenLogic.UpdateDisplayNodeFromVolumeNode(displayNode, MyinputVolume)

    # TODO Update volume rendering effect in real-time. 更新体绘制效果修改
    # volRenLogic = slicer.modules.volumerendering.logic()
    # MyinputVolume2 = slicer.mrmlScene.GetNodeByID('vtkMRMLScalarVolumeNode1')
    # displayNode = volRenLogic.CreateVolumeRenderingDisplayNode()
    # displayNode.UnRegister(volRenLogic)
    # slicer.mrmlScene.AddNode(displayNode)
    # MyinputVolume2.AddAndObserveDisplayNodeID(displayNode.GetID())
    # volRenLogic.UpdateDisplayNodeFromVolumeNode(displayNode, MyinputVolume2)

    # RenderingNode = slicer.util.getNode(MyinputVolume).Modified()
    # NewRenderingNode = RenderingNode.GetId()
    # volRenLogic = slicer.modules.volumerendering.logic()
    # displayNode = volRenLogic.GetFirstVolumeRenderingDisplayNode()

    logging.info('Processing completed')

    return True