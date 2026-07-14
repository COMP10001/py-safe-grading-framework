FROM archlinux:latest

RUN pacman-key --init
RUN pacman -Syu --noconfirm
RUN pacman -S python3 python-pip --noconfirm

COPY ./requirements.txt /requirements.txt
RUN python3 -m pip install -r requirements.txt --break-system-packages

COPY ./tests /home
COPY ./pysafegradingfw.py /home/pysafegradingfw.py
COPY ./ci-cd-test-runner.py /ci-cd-test-runner.py

CMD ["python3", "ci-cd-test-runner.py", "--docker", "--debug"]