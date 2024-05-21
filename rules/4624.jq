(: 
 Configure the $files_path variable!
:)

let $files_path := "./workbench/dataset/security*.ndjson"
for $event in json-file($files_path)
where $event.event.code = "4624"
return $event