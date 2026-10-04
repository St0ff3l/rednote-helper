import Foundation
import ObjectiveC
import Darwin
dlopen("/System/Library/PrivateFrameworks/WorkflowKit.framework/WorkflowKit", RTLD_NOW)
dlopen("/System/Library/PrivateFrameworks/ActionKit.framework/ActionKit", RTLD_NOW)
@objc class RunnerDelegate:NSObject {
 var finished=false
 @objc(workflowController:didFinishRunningWithError:cancelled:) func done(_ c:NSObject,_ error:NSError?,_ cancelled:Bool) { print("DONE",error?.description ?? "OK",cancelled);if let o=c.perform(NSSelectorFromString("output"))?.takeUnretainedValue(){print("OUTPUT",o)};finished=true }
 @objc(workflowController:didRunAction:error:) func action(_ c:NSObject,_ a:NSObject,_ error:NSError?) {print("ACTION",a.perform(NSSelectorFromString("identifier"))?.takeUnretainedValue() ?? "?",error?.description ?? "OK");if let o=a.perform(NSSelectorFromString("output"))?.takeUnretainedValue(){let s=String(describing:o);print("RESULT",String(s.prefix(1400)))}}
 @objc(userInterfaceForWorkflowController:) func ui(_ c:NSObject)->AnyObject? {return nil}
}
let reg=(NSClassFromString("WFActionRegistry") as! NSObject.Type).perform(NSSelectorFromString("sharedRegistry")).takeUnretainedValue() as! NSObject
let path=CommandLine.arguments.count>1 ? CommandLine.arguments[1]:"work/test-native.shortcut"
let doc=try PropertyListSerialization.propertyList(from:Data(contentsOf:URL(fileURLWithPath:path)),options:[],format:nil) as! [String:Any]
var acts:[NSObject]=[]
for item in doc["WFWorkflowActions"] as! [[String:Any]] {
 let a=reg.perform(NSSelectorFromString("createActionWithIdentifier:serializedParameters:"),with:item["WFWorkflowActionIdentifier"],with:item["WFWorkflowActionParameters"]).takeUnretainedValue() as! NSObject
 acts.append(a)
}
let workflow=(NSClassFromString("WFWorkflow") as! NSObject.Type).init()
workflow.perform(NSSelectorFromString("setName:"),with:"XHS Local Test")
workflow.perform(NSSelectorFromString("setActions:"),with:acts)
let controller=(NSClassFromString("WFWorkflowController") as! NSObject.Type).init()
controller.perform(NSSelectorFromString("setWorkflow:"),with:workflow)
let delegate=RunnerDelegate()
controller.perform(NSSelectorFromString("setDelegate:"),with:delegate)
controller.perform(NSSelectorFromString("run"))
let deadline=Date().addingTimeInterval(25)
while !delegate.finished && Date()<deadline {RunLoop.current.run(until:Date().addingTimeInterval(0.1))}
if !delegate.finished {print("TIMEOUT")}
