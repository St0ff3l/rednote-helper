import Foundation
import ObjectiveC
import Darwin
dlopen("/System/Library/PrivateFrameworks/WorkflowKit.framework/WorkflowKit", RTLD_NOW)
dlopen("/System/Library/PrivateFrameworks/ActionKit.framework/ActionKit", RTLD_NOW)
let cls=NSClassFromString("WFActionRegistry") as! NSObject.Type
let reg=cls.perform(NSSelectorFromString("sharedRegistry")).takeUnretainedValue() as! NSObject
let doc=try PropertyListSerialization.propertyList(from:Data(contentsOf:URL(fileURLWithPath:"work/xhs-unsigned.shortcut")),options:[],format:nil) as! [String:Any]
for (i,item) in (doc["WFWorkflowActions"] as! [[String:Any]]).enumerated() {
 let id=item["WFWorkflowActionIdentifier"] as! String
 let a=reg.perform(NSSelectorFromString("createActionWithIdentifier:serializedParameters:"),with:id,with:item["WFWorkflowActionParameters"]).takeUnretainedValue() as! NSObject
 let isMissingSel=NSSelectorFromString("isMissing")
 typealias BoolGetter = @convention(c) (AnyObject,Selector)->Bool
 let missing=unsafeBitCast(a.method(for:isMissingSel),to:BoolGetter.self)(a,isMissingSel)
 print(i,id,missing ? "MISSING":"OK")
 if id.contains("conditional") {print(a.perform(NSSelectorFromString("serializedParameters")).takeUnretainedValue())}
}
