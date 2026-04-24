#!/bin/bash
# AI 日报 cron 定时任务脚本

# 每日 9:00 执行
0 9 * * * /home/donna/Hermes/workspace/projects/ai-daily-report-V1-0424/run.sh >> /home/donna/Hermes/workspace/projects/ai-daily-report-V1-0424/logs/cron.log 2>&1
