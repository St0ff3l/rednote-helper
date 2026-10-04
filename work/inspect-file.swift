import Foundation
import ObjectiveC
import Darwin
dlopen("/System/Library/PrivateFrameworks/WorkflowKit.framework/WorkflowKit", RTLD_NOW)
dlopen("/System/Library/PrivateFrameworks/ActionKit.framework/ActionKit", RTLD_NOW)
for n in ["WFShortcutFile","WFShortcut","WFShortcutSerialization","WFWorkflowFile"] {
 guard let c = NSClassFromString(n) else { print(n,"missing");continue }
 print("CLASS",n)
 for x in [c,object_getClass(c)!] {
 var count:UInt32=0
 if let ms=class_copyMethodList(x,&count) {for i in 0..<Int(count) { print(NSStringFromSelector(method_getName(ms[i]))) };free(ms)}
 }
}
