### WebCompiler ���
WebCompiler ��һ�����ڱ���Ͳ���web��Ŀ��python�ű����е�����java��ant���ߣ�֧�ֱ����ʱ�����Ŀ¼���ƣ������滻��js/css/htmlѹ���ȹ��ܡ�


### �����ļ�config.json˵��
{
    // �ļ����Ͱ�����
    "allowext" : ["png", "jpg", "jpeg", "gif", "js", "css", "html", "htm", "manifest"],
    // �����ļ�����Ŀ¼���·��; '.'  => ��ǰ������Ŀ¼
    "relPath" : "./public/",
    // ���빤��·��
    "tools" : {
        // js compiler
        "googleclosurePath" : "../tools/compiler.jar",
        // css compiler
        "yuicompiressorPath" : "../tools/yuicompressor-2.4.6.jar",
        // html template extractor
        "htmlTmplExtractPath" : "../tools/htmlTemplateExtractor.py"
    },
    // ֧���Զ�����
    "cmarks": {
        "%module%" : "compiler"
    },
    // �������
    // �ļ�������
    //    -source:���룬Դ��ַ
    //    -target:���룬Ŀ���ַ
    //    -level: ��ѡ���������ȼ������ȼ�Խ�ߣ�Խ����룬Ĭ�����ȼ�Ϊ0
    //    -version:��ѡ���Ƿ���Ӱ汾�ţ�Ĭ��Ϊ�ļ�����汾�ţ���subversionΪtrueʱ��ʹ�� '���ļ��汾-���ļ��汾���ֵ' ��Ϊ�汾�ţ����ļ���
    //    -subversion:��ѡ���Ƿ�����������Դ�İ汾�ţ��Ƿ���Ҫ�����ļ����������Դ�İ汾��
    //    -subtype:��ѡ�������Դ������ ['image'] ͼƬ�� ['json'] �������ͣ�['js'] js�ļ� , ['css'] css�ļ�
    //    -compress:��ѡ���Ƿ����ѹ��
    //    -markreplace:��ѡ�����ݻ���·���Ƿ��а汾��ʱ����滻��� [boolean]��֧�ֵ�mark����  ��ǰ���� '%Date%' svn����������: '%LastUpdate%' �汾��: '%Version%' ʱ��� '%TimeStamp%' �ɰ���cmarks
    //    -extracttmpl: html ��ȡģ�浽js������js��ģ���ļ���ģ���滻���δ "%HtmlTemplates%"����ʱ��֧���Զ���
    //    -extractto: html ��ȡģ�浽js������jsĿ���ļ�
    // Qzmin������
    //    -source:
    //    -target:
    //    -level: 
    //    -compress:
    //    -version:
    // �ļ��������� (�ļ��й���source,target������/��β)
    //    -source:
    //    -target:
    //    -level:
    //    -compress:
    //    -version:
    //    -subversion:
    //    -subtype:
    //    -recursive:��ѡ���Ƿ�ݹ���Ŀ¼
    //    -ext:��ѡ����չ��������
    //    -blacklist:��ѡ���ļ���������
    //    -whitelist:��ѡ���ļ���������
    //    -markreplace:
    //    -relpath:��ѡ������ļ�target���Ŀ¼�����ȼ�����ȫ��relPath
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
    // ����ģʽ(����ģʽ����������ñ������, ִ��˳���) , �ƶ��������󽫻���Թ����е� level �������ȼ�����
    "modes" : {
        "default": ["images"]
    }
}