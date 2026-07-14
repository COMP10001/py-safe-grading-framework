FROM archlinux:latest

RUN pacman-key --init
RUN pacman -Syu --noconfirm
RUN pacman -S python3 python-pip --noconfirm

COPY ./requirements.txt /requirements.txt
RUN python3 -m pip install -r requirements.txt --break-system-packages

COPY ./tests /home
COPY ./pysafegradingfw.py /pysafegradingfw.py
COPY ./ci-cd-test-runner.py /ci-cd-test-runner.py
RUN mkdir /home/current_feedback

CMD ["python3", "ci-cd-test-runner.py", "--docker"]
# CMD ["python3", "ci-cd-test-runner.py", "--docker", "--debug"]