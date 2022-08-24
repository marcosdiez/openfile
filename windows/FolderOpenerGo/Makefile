BINARY_NAME=folderOpener
SOURCE_FILES=folderOpener.go

all: ${BINARY_NAME}


${BINARY_NAME}: ${SOURCE_FILES}
	go fmt ${SOURCE_FILES}
	go build -o ${BINARY_NAME} ${SOURCE_FILES}

${BINARY_NAME}.exe: ${SOURCE_FILES}
	GOOS=windows go build -o ${BINARY_NAME}.exe ${SOURCE_FILES}

build: ${BINARY_NAME} ${BINARY_NAME}.exe
# 	echo "xpto"
# 	go build -o ${BINARY_NAME} ${SOURCE_FILES}

run: ${BINARY_NAME}
	./${BINARY_NAME}

clean:
	go clean
	rm -f ${BINARY_NAME} ${BINARY_NAME}.exe
