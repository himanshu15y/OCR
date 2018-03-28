path="$1"
echo path="$path"
filename=`ls -rt "$path" | tail -1`
echo filename=$filename
python ExtractTest1.py "${path}/$filename" $2
