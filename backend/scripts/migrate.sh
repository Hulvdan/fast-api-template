input_variable=$1

case $input_variable in
  '--help')
    echo "This is a help to use migrate command"
    echo "--help or -h will show help"
    echo "Also you can use this input to introduce revision or head"
    break
    ;;
  *)
    PYTHONPATH=$(pwd)
    echo $PYTHONPATH
    alembic upgrade $input_variable
    break
    ;;
esac
