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
    # output volume selector
    #
    # self.outputSelector = slicer.qMRMLNodeComboBox()
    # self.outputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    # self.outputSelector.selectNodeUponCreation = True
    # self.outputSelector.addEnabled = True
    # self.outputSelector.removeEnabled = True
    # self.outputSelector.noneEnabled = True
    # self.outputSelector.showHidden = False
    # self.outputSelector.showChildNodeTypes = False
    # self.outputSelector.setMRMLScene( slicer.mrmlScene )
    # self.outputSelector.setToolTip( "Pick the output to the algorithm." )
    # parametersFormLayout.addRow("Output Volume: ", self.outputSelector)

    #
    # threshold value  阈值滑块
    #
    # self.imageThresholdSliderWidget = ctk.ctkSliderWidget()
    # self.imageThresholdSliderWidget.singleStep = 0.1
    # #self.imageThresholdSliderWidget.minimum = -100
    # self.imageThresholdSliderWidget.minimum = 0
    # self.imageThresholdSliderWidget.maximum = 1000
    # self.imageThresholdSliderWidget.value = 0.5
    # self.imageThresholdSliderWidget.setToolTip("Set Lower threshold value for computing the output image. Voxels that have intensities lower than this value will set to zero.")
    # parametersFormLayout.addRow("Lower:", self.imageThresholdSliderWidget)
    #
    # self.imageThresholdSliderWidget2 = ctk.ctkSliderWidget()
    # self.imageThresholdSliderWidget2.singleStep = 0.1
    # # self.imageThresholdSliderWidget.minimum = -100
    # self.imageThresholdSliderWidget2.minimum = 0
    # self.imageThresholdSliderWidget2.maximum = 1000
    # self.imageThresholdSliderWidget2.value = 100
    # self.imageThresholdSliderWidget2.setToolTip(
    #   "Set Upper threshold value for computing the output image. Voxels that have intensities lower than this value will set to zero.")
    # parametersFormLayout.addRow("Upper:", self.imageThresholdSliderWidget2)

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
    # 复选框
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

    # connections            点击按钮触发onApplyButton函数完成阈值化的功能
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    # self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer    Apply按钮下方的空白间隔
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  def cleanup(self):
    pass

  def onSelect(self):
    # self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()
    self.applyButton.enabled = self.inputSelector.currentNode()



  # 点击按钮之后触发onApplyButton函数，然后传输入体，输出体，滑块值到其中的logic(ScriptedLoadableModuleTemplateLogic)并执行logic
  # self.inputSelector.currentNode() 是输入volume 相当于是 masterVolumeNode
  def onApplyButton(self):
    logic = ScriptedLoadableModuleTemplateLogic()
   #enableScreenshotsFlag = self.enableScreenshotsFlagCheckBox.checked
   #LowerimageThreshold = self.imageThresholdSliderWidget.value
   #UpperimageThreshold = self.imageThresholdSliderWidget2.value

    LowerimageThreshold2 = self.thresholdRangeSlider1.minimumValue
    UpperimageThreshold2 = self.thresholdRangeSlider1.maximumValue

   #logic.run(self.inputSelector.currentNode(), self.outputSelector.currentNode(), imageThreshold, enableScreenshotsFlag)
   #logic.run(self.inputSelector.currentNode(), self.outputSelector.currentNode(), imageThreshold)
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
  这个类应该实现所有的实际由模块完成的计算。
  接口应该是这样的，其他 python 代码可以导入这个类并使用该功能，而无需 Widget 的实例。
  重点是run()
  """

  # def hasImageData(self,volumeNode):
  #   """This is an example logic method that
  #   returns true if the passed in volume
  #   node has valid image data
  #   """
  #   if not volumeNode:
  #     logging.debug('hasImageData failed: no volume node')
  #     return False
  #   if volumeNode.GetImageData() is None:
  #     logging.debug('hasImageData failed: no image data in volume node')
  #     return False
  #   return True



  # def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
  #   """Validates if the output is not the same as input
  #   """
  #   if not inputVolumeNode:
  #     logging.debug('isValidInputOutputData failed: no input volume node defined')
  #     return False
  #   if not outputVolumeNode:
  #     logging.debug('isValidInputOutputData failed: no output volume node defined')
  #     return False
  #   if inputVolumeNode.GetID()==outputVolumeNode.GetID():
  #     logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
  #     return False
  #   return True

  # 比如这里的inputVolume其实就是self.inputSelector.currentNode()
  def run(self, inputVolume, LowerimageThreshold2, UpperimageThreshold2):
    """
    Run the actual algorithm
    执行实际的算法实现相应的功能
    """

    # if not self.isValidInputOutputData(inputVolume, outputVolume):
    #   slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
    #   return False

    # input volume 和 output volume 都没问题之后就在控制台打印  处理开始
    logging.info('Processing started')

    # 阈值化分割操作  The Segmentation after thresholding
    # Compute the thresholded output volume using the Threshold Scalar Volume CLI module
    # 用 Threshold Scalar Volume CLI 模块计算阈值
    # cliParams = {'InputVolume': inputVolume.GetID(), 'OutputVolume': outputVolume.GetID(), 'ThresholdValue' : imageThreshold, 'ThresholdType' : 'Above'}
    # cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True)
    MyinputVolume = inputVolume.GetName()
    voxelArray = slicer.util.array(MyinputVolume)
    voxelArray[voxelArray < LowerimageThreshold2] = 0
    voxelArray[voxelArray > UpperimageThreshold2] = 0
    slicer.util.getNode(MyinputVolume).Modified()

    #Surface Extraction 表面提取
    # Set the current node as the masterVolumeNode for surface extraction
    # masterVolumeNode = slicer.util.getNode(self.inputSelector.currentNode().GetName())
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

    # TODO 更新体绘制效果修改 Update volume rendering effect in real-time.
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

#
# class ScriptedLoadableModuleTemplateTest(ScriptedLoadableModuleTest):
#   """
#   This is the test case for your scripted module.
#   Uses ScriptedLoadableModuleTest base class, available at:
#   https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
#   """
#
#   def setUp(self):
#     """ Do whatever is needed to reset the state - typically a scene clear will be enough.
#     """
#     slicer.mrmlScene.Clear(0)
#
#   def runTest(self):
#     """Run as few or as many tests as needed here.
#     """
#     self.setUp()
#     self.test_ScriptedLoadableModuleTemplate1()
#
#   def test_ScriptedLoadableModuleTemplate1(self):
#     """ Ideally you should have several levels of tests.  At the lowest level
#     tests should exercise the functionality of the logic with different inputs
#     (both valid and invalid).  At higher levels your tests should emulate the
#     way the user would interact with your code and confirm that it still works
#     the way you intended.
#     One of the most important features of the tests is that it should alert other
#     developers when their changes will have an impact on the behavior of your
#     module.  For example, if a developer removes a feature that you depend on,
#     your test should break so they know that the feature is needed.
#     """
#
#     self.delayDisplay("Starting the test")
#     #
#     # first, get some data
#     #
#     import SampleData
#     volumeNode = SampleData.downloadFromURL(
#       nodeNames='MRHead',
#       fileNames='MR-head.nrrd',
#       uris=TESTING_DATA_URL + 'SHA256/cc211f0dfd9a05ca3841ce1141b292898b2dd2d3f08286affadf823a7e58df93',
#       checksums='SHA256:cc211f0dfd9a05ca3841ce1141b292898b2dd2d3f08286affadf823a7e58df93')
#     self.delayDisplay('Finished with download and loading')
#
#     logic = ScriptedLoadableModuleTemplateLogic()
#     self.assertIsNotNone( logic.hasImageData(volumeNode) )
#     self.takeScreenshot('ScriptedLoadableModuleTemplateTest-Start','MyScreenshot',-1)
#     self.delayDisplay('Test passed!')
