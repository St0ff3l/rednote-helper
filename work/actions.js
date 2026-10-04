ObjC.import('/System/Library/PrivateFrameworks/WorkflowKit.framework');
ObjC.import('/System/Library/PrivateFrameworks/ActionKit.framework');
var r=$.WFActionRegistry.sharedRegistry;
var ids=['downloadurl','matchtext','gettext','getvalueforkey','replace.text','getgroupfrommatchedtext','getclipboard','geturlfrominput','getitemfromlist','conditional','repeat.each','savetocameraroll','ask','alert','exit','choosefromlist','setvariable','getvariable'];
var out={};
ids.forEach(function(id){try{var a=r.createActionWithIdentifierSerializedParameters('is.workflow.actions.'+id,$({}));out[id]=ObjC.deepUnwrap(a.definition)}catch(e){out[id]=String(e)}});
JSON.stringify(out);
