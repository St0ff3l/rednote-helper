import Foundation
import ObjectiveC
import Darwin
dlopen("/System/Library/PrivateFrameworks/WorkflowKit.framework/WorkflowKit", RTLD_NOW)
dlopen("/System/Library/PrivateFrameworks/ActionKit.framework/ActionKit", RTLD_NOW)
let c=NSClassFromString("WFActionRegistry") as! NSObject.Type
let r=c.perform(NSSelectorFromString("sharedRegistry")).takeUnretainedValue() as! NSObject
let ids=["setitemname","getitemname","getname","choosefrommenu","list","properties.files","getimagesfrominput"]
var out:[String:Any]=[:]
for id in ids {
 if let a=r.perform(NSSelectorFromString("createActionWithIdentifier:serializedParameters:"),with:"is.workflow.actions."+id,with:[:]).takeUnretainedValue() as? NSObject {
  var vals:[String:Any]=[:]
  for key in ["serializedParameters","inputParameterKey","localizedName"] {if let v=a.perform(NSSelectorFromString(key))?.takeUnretainedValue(){vals[key]=v}}
  if let def=a.perform(NSSelectorFromString("definition"))?.takeUnretainedValue() as? NSObject {
  if let ps=a.perform(NSSelectorFromString("parameterDefinitions"))?.takeUnretainedValue() {if let arr=ps as? [NSObject] { vals["params"]=arr.map { p -> [String:Any] in
    var pd:[String:Any]=[:]
    for key in ["Key","Class","Label","DefaultValue","Items"] {if let v=p.perform(NSSelectorFromString("objectForKey:"),with:key)?.takeUnretainedValue() {pd[key]=v}}
    return pd
   }}}
  }
  out[id]=vals
 }
}
func clean(_ v:Any)->Any {
 if let d=v as? [String:Any] { return d.mapValues {clean($0)} }
 if let a=v as? [Any] {return a.map {clean($0)}}
 if v is String || v is NSNumber || v is NSNull {return v}
 return String(describing:v)
}
let data=try JSONSerialization.data(withJSONObject:clean(out),options:[.prettyPrinted,.sortedKeys])
print(String(data:data,encoding:.utf8)!)
