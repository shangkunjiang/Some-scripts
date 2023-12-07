# 定义序号类型 
set C "name 1"
set Pt "serial 4081"

# 计算Pt-C

# 定义rdf第1个原子 Pt
set selection1 "$Pt"
# 定义rdf第2个原子 C
set selection2 "$C"
# rdf相关参数定义
set rdf [measure gofr [atomselect top $selection1] [atomselect top $selection2] delta 0.1 rmax 30 usepbc true selupdate false first 0 last -1 step 1]
#定义distence，存入列表
set distance [lindex $rdf 0]
#定义gr，存入列表
set gr [lindex $rdf 1]
#定义CN，存入列表
set CN [lindex $rdf 2]
     
# 写入文件 gr
# 定义文件名
set gr_file_name {rdf-Pt-C.dat}
# 生成输出文件
set gr_file [open $gr_file_name w]
# 循环写入，避免单行
foreach {a} $distance {b} $gr {c} $CN { 
    set data [format "%s %s %s" $a $b $c] 
    puts $gr_file $data }
# 必须关闭文件，否则写入数据不显示
close $gr_file
