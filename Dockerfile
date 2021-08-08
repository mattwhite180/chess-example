FROM python:3.10.0b3-buster AS basedependencies
ENV TZ="America/Denver"

EXPOSE 8000

WORKDIR /root/

RUN apt-get update -y \                                                                                        
    && apt-get install -y \                                                                                    
	python3-pip \
	build-essential \
	procps \
	curl \
	file \
	git \
	sudo \
    libopenblas-dev \
    ninja-build \
    libgtest-dev \
    libstdc++-8-dev \
    clang-6.0 \
    pkg-config \
	meson \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip setuptools wheel
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

##############
# stockfish
FROM basedependencies AS stockfish
RUN mkdir /root/stockfish/
WORKDIR /root/stockfish/
RUN wget https://stockfishchess.org/files/stockfish_14_linux_x64.zip
RUN unzip stockfish_14_linux_x64.zip
###############


##############
# leela lc0
FROM stockfish AS leela
WORKDIR /root/
RUN git clone -b release/0.27 https://github.com/LeelaChessZero/lc0
WORKDIR /root/lc0/
RUN bash build.sh
WORKDIR /root/lc0/build/release/
COPY weights_run2_744679.pb.gz .
########

FROM leela
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY chessgame.py .


CMD python3 chessgame.py