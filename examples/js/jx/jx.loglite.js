/* == jx.loglite 简单log =============================================
 * Copyright (c) 2010, Tencent.com All rights reserved.
 * version: 1.0
 * rehorn
 * -------------------------------------------- 2012-1-10 ----- */
 
Jx().$package(function (J) {
    var $D = J.dom,
		$E = J.event,
		$S = J.string,
		packageContext = this;
	
	var isDebug = false;
	
	//var onDomReady = function(){
//		if(isDebug){
//			var html = '\
//				<h5 style="font:bold 12px/20px calibri; margin:0; padding:0;">\
//					<a id="consoleMin" href="javascript:void(0);" style="float:right; text-decoration:none; color:red; display:none;" onclick="document.getElementById(\'consoleText\').style.display=\'none\';document.getElementById(\'consoleMin\').style.display=\'none\';document.getElementById(\'consoleRes\').style.display=\'\';return false;">×</a>\
//					<a id="consoleRes" href="javascript:void(0);" style="float:left; text-decoration:none; color:red;" ondblclick="document.getElementById(\'consoleText\').style.display=\'\';document.getElementById(\'consoleMin\').style.display=\'\';document.getElementById(\'consoleRes\').style.display=\'none\';return false;">^</a>\
//				</h5>\
//				<textarea id="consoleText" style="display:none; width:310px;height:230px;font:9px Simsun,Consolas,Arial;border: 1px solid #8EC1DA; border-radius: 5px;background: #DDEEF6;padding: 5px;outline: 0;"></textarea>\
//				';
//			var node = $D.node('div', {
//				'id': 'console',
//				'style': 'width:320px; position:fixed; bottom:10px; left:14px;'	
//			});
//			node.innerHTML = html;
//			$D.getDoc().body.appendChild(node);
//			
//			console = console || {};
//			console.info=function(){
//				var el=$D.id('consoleText');
//				var now = '[' + J.date.format(new Date(), 'hh:mm:ss') + ']';
//				el.value+='>> '+Array.prototype.concat.apply([now],arguments)+'\n';
//			};
//			console.log=function(object){
//				var el=$D.id('consoleText');
//				var now = '[' + J.date.format(new Date(), 'hh:mm:ss') + ']';
//				el.value+='>> ' + now + ', ' + JSON.stringify(object) +'\n';
//			};
//			
//			console.info('log start');
//		}else{
//			console = {};
//			console.info = function(){};
//			console.log = function(){};
//		}
//		
//		J.consoleLite = console;
	//};
	
	//$E.onDomReady(onDomReady);
});