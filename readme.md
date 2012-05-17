### WebCompiler 简介
WebCompiler 是一个用于编译和部署web项目的python脚本，有点类似java的ant工具，支持编译的时候进行目录复制，变量替换，js/css/html压缩等功能。


### 配置文件config.json说明
{
    // 文件类型白名单
    "allowext" : ["png", "jpg", "jpeg", "gif", "js", "css", "html", "htm", "manifest"],
    // 编译文件存在目录相对路径; '.'  => 当前的运行目录
    "relPath" : "./public/",
    // 编译工具路径
    "tools" : {
        // js compiler
        "googleclosurePath" : "../tools/compiler.jar",
        // css compiler
        "yuicompiressorPath" : "../tools/yuicompressor-2.4.6.jar",
        // html template extractor
        "htmlTmplExtractPath" : "../tools/htmlTemplateExtractor.py"
    },
    // 支持自定义标记
    "cmarks": {
        "%module%" : "compiler"
    },
    // 编译规则
    // 文件配置项
    //    -source:必须，源地址
    //    -target:必须，目标地址
    //    -level: 可选，编译优先级，优先级越高，越早编译，默认优先级为0
    //    -version:可选，是否添加版本号（默认为文件本身版本号，当subversion为true时，使用 '本文件版本-子文件版本最大值' 作为版本号）到文件名
    //    -subversion:可选，是否依赖其他资源的版本号，是否需要更新文件内容相关资源的版本号
    //    -subtype:可选，相关资源的类型 ['image'] 图片， ['json'] 配置类型，['js'] js文件 , ['css'] css文件
    //    -compress:可选，是否进行压缩
    //    -markreplace:可选，内容或者路径是否有版本、时间戳替换标记 [boolean]，支持的mark类型  当前日期 '%Date%' svn最后更新日期: '%LastUpdate%' 版本号: '%Version%' 时间戳 '%TimeStamp%' 可按照cmarks
    //    -extracttmpl: html 抽取模版到js，生成js的模版文件，模版替换标记未 "%HtmlTemplates%"，暂时不支持自定义
    //    -extractto: html 抽取模版到js，生成js目标文件
    // Qzmin配置项
    //    -source:
    //    -target:
    //    -level: 
    //    -compress:
    //    -version:
    // 文件夹配置项 (文件夹规则source,target必须以/结尾)
    //    -source:
    //    -target:
    //    -level:
    //    -compress:
    //    -version:
    //    -subversion:
    //    -subtype:
    //    -recursive:可选，是否递归子目录
    //    -ext:可选，扩展名白名单
    //    -blacklist:可选，文件名黑名单
    //    -whitelist:可选，文件名白名单
    //    -markreplace:
    //    -relpath:可选，输出文件target相对目录，优先级高于全局relPath
    "rules" : {
        "images" : {
            "source" : "./images/",
            "target" : "./cdn/%module%/images/",
            "recursive" : 1
        },
        "whitelist" : {
            "source" : "./res/",
            "target" : "./cdn/%module%/res/",
            "whitelist" : ["whitelist.js"]
        },
        "filecopy" : {
            "source" : "./res/filecopy.js",
            "target" : "./cdn/%module%/res/filecopy-publish.js"
        },
        "javascript": {
            "source" : "./js/",
            "target" : "./cdn/%module%/js/"
        },
        "jx.qzmin": {
            "source" : "./js/jx.custom.js.qzmin",
            "target" : "./cdn/%module%/js/jx.custom.js",
            "compress" : 1
        },
        "css" : {
            "source" : "./css/",
            "target" : "./cdn/%module%/css/"
        },
        "html" : {
            "source" : "./",
            "target" : "./webserver/%module%/",
            "ext": ["html"]
        },
        "html.extract" : {
            "source" : "./index.html",
            "target" : "./webserver/%module%/index.html",
            "extracttmpl" : "./tools/templates.js.tmpl",
            "extractto" : "./js/emplates.js"
        },
        "manifest" : {
            "source" : "./",
            "target" : "./webserver/%module%/",
            "ext": ["manifest"],
            "whitelist": ["cache.manifest"],
            "markreplace": 1
        }
    },
    // 编译模式(编译模式的数组可配置编译规则, 执行顺序等) , 制定编译规则后将会忽略规则中的 level 编译优先级设置
    "modes" : {
        "default": ["images"]
    }
}