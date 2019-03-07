require(["jquery","underscore","backbone","splunk.util","views/shared/controls/SyntheticRadioControl"],function(__WEBPACK_EXTERNAL_MODULE_1__,__WEBPACK_EXTERNAL_MODULE_2__,__WEBPACK_EXTERNAL_MODULE_10__,__WEBPACK_EXTERNAL_MODULE_18__,__WEBPACK_EXTERNAL_MODULE_30__){return function(modules){function __webpack_require__(moduleId){if(installedModules[moduleId])return installedModules[moduleId].exports;var module=installedModules[moduleId]={exports:{},id:moduleId,loaded:!1};return modules[moduleId].call(module.exports,module,module.exports,__webpack_require__),module.loaded=!0,module.exports}var installedModules={};return __webpack_require__.m=modules,__webpack_require__.c=installedModules,__webpack_require__.p="",__webpack_require__(0)}({0:function(module,exports,__webpack_require__){var __WEBPACK_AMD_DEFINE_ARRAY__,__WEBPACK_AMD_DEFINE_RESULT__;__WEBPACK_AMD_DEFINE_ARRAY__=[__webpack_require__(2),__webpack_require__(1),__webpack_require__(10),__webpack_require__(18),__webpack_require__(30)],__WEBPACK_AMD_DEFINE_RESULT__=function(_,$,Backbone,utils,SyntheticRadioControl){$(".viz").hide(),this.model=this.model||{},this.model.state=new Backbone.Model({showHeatMap:!1,selectedGroup:"all",relatedTo:""});var heat_map_toggle=new SyntheticRadioControl({model:this.model.state,modelAttribute:"showHeatMap",items:[{label:_("Column Chart").t(),value:!1},{label:_("Heat Map").t(),value:!0}]});$("#indexer_count_by_tcp_input_queue_fill_ratio .heatmap_toggle").append(heat_map_toggle.render().$el),$("#indexer_count_by_tcp_input_queue_fill_ratio .heatmap_toggle .btn-group .btn").click(function(){"true"==this.getAttribute("data-value")?($("#indexer_count_by_tcp_input_queue_fill_ratio .viz").show(),$("#indexer_count_by_tcp_input_queue_fill_ratio .chart").hide()):"false"==this.getAttribute("data-value")&&($("#indexer_count_by_tcp_input_queue_fill_ratio .viz").hide(),$("#indexer_count_by_tcp_input_queue_fill_ratio .chart").show())})}.apply(exports,__WEBPACK_AMD_DEFINE_ARRAY__),!(void 0!==__WEBPACK_AMD_DEFINE_RESULT__&&(module.exports=__WEBPACK_AMD_DEFINE_RESULT__))},1:function(module,exports){module.exports=__WEBPACK_EXTERNAL_MODULE_1__},2:function(module,exports){module.exports=__WEBPACK_EXTERNAL_MODULE_2__},10:function(module,exports){module.exports=__WEBPACK_EXTERNAL_MODULE_10__},18:function(module,exports){module.exports=__WEBPACK_EXTERNAL_MODULE_18__},30:function(module,exports){module.exports=__WEBPACK_EXTERNAL_MODULE_30__}})});