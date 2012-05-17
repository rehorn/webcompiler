import re, json, getopt, sys

result = {}

def replacefunc(m):
    result[m.group(1)] = re.sub('\n|\r', '', m.group(2))

if __name__ == '__main__':
    print 'start extract html template to js', 60 * '-'

    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:t:j:", ["inputFile=", "outputFile=", "inputJsFile=", "outputJsFile="])
    except getopt.GetoptError, err:
        print str(err)

    for o, a in opts:
        if o in ("-i", "--inputFile"):
            inputFile = a
        if o in ("-o", "--outputFile"):
            outputFile = a
        if o in ("-t", "--inputJsFile"):
            inputJsFile = a
        if o in ("-j", "--outputJsFile"):
            outputJsFile = a

    input = open(inputFile)
    content = input.read()
    #print content
    #for line in f.readlines():
    #   content += line
    input.close()
    p = re.compile('<script\s*id="(\w+)"\s*type="text\/plain"\s*>([\s\S]*?)<\/script>',re.I)
    content = p.sub(replacefunc,content)

    output = open(outputFile, 'w')
    output.write(content)
    output.close()

    input = open(inputJsFile)
    content = input.read()
    input.close()

    result = json.dumps(result)
    content = re.sub('"%HtmlTemplates%"', result, content)

    output = open(outputJsFile, 'w')
    output.write(content)
    output.close()
    print 'extract html template to ', outputJsFile

    print 'extract template code done'
