FROM python:3.7.16-slim-bullseye

RUN apt update && apt install -y \
    rtl-433 \
    git

RUN git clone https://github.com/mcbridejc/monitor_rtl433.git /monitor_rtl433
WORKDIR /monitor_rtl433
RUN pip3 install .

ENTRYPOINT ["python3", "-m", "monitor_rtl433"]