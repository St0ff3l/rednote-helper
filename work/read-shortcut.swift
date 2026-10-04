import Foundation
import ObjectiveC
import Darwin
dlopen("/System/Library/PrivateFrameworks/WorkflowKit.framework/WorkflowKit", RTLD_NOW)
let cls=NSClassFromString("WFWorkflowFile") as! NSObject.Type
let obj=cls.perform(NSSelectorFromString("alloc")).takeUnretainedValue() as! NSObject
let selector=NSSelectorFromString("initWithFileData:name:error:")
typealias Init = @convention(c) (AnyObject,Selector,NSData,NSString,UnsafeMutablePointer<NSError?>)->AnyObject?
var error:NSError?
let data=try Data(contentsOf:URL(fileURLWithPath:CommandLine.arguments[1])) as NSData
if let f=unsafeBitCast(obj.method(for:selector),to:Init.self)(obj,selector,data,"reference",&error) as? NSObject,
 let root=f.perform(NSSelectorFromString("rootObject"))?.takeUnretainedValue() {
 let b=try PropertyListSerialization.data(fromPropertyList:root,format:.xml,options:0)
 try b.write(to:URL(fileURLWithPath:CommandLine.arguments[2]))
 print("Decoded")
} else {print(error?.description ?? "nil")}
