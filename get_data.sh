mkdir data
kaggle datasets download stackoverflow/rquestions -p data --unzip
echo "Converting answers CSV to Sqlite"
cd data
csv-to-sqlite -f Answers.csv -o answers.sqlite
