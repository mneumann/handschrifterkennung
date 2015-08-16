FETCH=wget
BASE=http://yann.lecun.com/exdb/mnist
FILES="train-images-idx3-ubyte \
       train-labels-idx1-ubyte \
       t10k-images-idx3-ubyte \
       t10k-labels-idx1-ubyte"

mkdir -p datasets
cd datasets

for file in ${FILES}; do
    if [ ! -e "${file}" ]; then
        echo "fetching ${file}.gz"
        ${FETCH} ${BASE}/${file}.gz
        gunzip ${file}.gz
    fi
done
