import Foundation
import ObjectiveC
import Darwin
dlopen("/System/Library/PrivateFrameworks/WorkflowKit.framework/WorkflowKit", RTLD_NOW)
for name in ["WFWorkflowControllerDelegate","WFWorkflowControllerRunningDelegate"] {
 if let p=objc_getProtocol(name) {print(name);for req in [true,false]{var count:UInt32=0;if let ms=protocol_copyMethodDescriptionList(p,req,true,&count){for i in 0..<Int(count){print(String(cString:ms[i].types!),NSStringFromSelector(ms[i].name!))}}}}
}
