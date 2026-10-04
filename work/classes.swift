import Foundation
import ObjectiveC
import Darwin
dlopen("/System/Library/PrivateFrameworks/WorkflowKit.framework/WorkflowKit", RTLD_NOW)
dlopen("/System/Library/PrivateFrameworks/ActionKit.framework/ActionKit", RTLD_NOW)
var count:UInt32=0
let list=objc_copyClassList(&count)!
for i in 0..<Int(count) {
 let n=NSStringFromClass(list[i])
 if n.hasPrefix("WF") && ["Repeat","Variable","WorkflowRunner","WorkflowExecution","Workflow"].contains(where:{n.contains($0)}) && !n.contains("View") && !n.contains("UI") {print(n)}
}
