# -*- coding: utf-8 -*-
# word批量转换txt(utf-8)
# Tianqi Wang (tianqi.wang@sjtu.edu.cn)

import docx

def file_path_generate(start_index, batch, file_path_constant):
    file_path_list = []
    for i in range(batch):
        index = start_index + i
        file_path = file_path_constant + str(index) + '.docx'
        file_path_list = file_path_list + [file_path]
    return file_path_list

def word2txt(file_path_list, start_index):
    for i in range(len(file_path_list)):
        text_content = []
        file = docx.Document(file_path_list[i])
        for para in file.paragraphs:
            para_content = para.text
            text_content = text_content + [para_content]
        
        output_name = str(start_index + i) + '.txt'
        f = open(output_name, 'a')
        for j in range(len(text_content)):
            f.write(text_content[j].encode('utf-8'))
            f.write('\n')
        f.close()
   
if __name__ == '__main__':
    startIndex = 1
    batch = 20   # 每N个文档转换一次
    filePathConstant = '/Users/apple/Desktop/law_corpus_word/'
    filePathList = file_path_generate(startIndex, batch, filePathConstant)
    word2txt(filePathList, startIndex)
    print 'Complete'
