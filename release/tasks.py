from django.core.mail import EmailMessage
from time import sleep
import traceback
from utils.jenkins_api import JenkinsApi
from opsbox.celery import app
from .models import Deploy

@app.task(name='deploy')
def codedeploy(id):
    """
    后台执行上线任务（后台jenkins构建任务）
    :param deploy: Deploy实例(申请上线会往数据库里插一条记录，传过来的就是这条记录）
    :return:
    """
    jenkins = JenkinsApi()
    dep = Deploy.objects.get(id=id)
    name = dep.projectname.name + "/" + dep.webname.name
    number = jenkins.get_next_build_number(name)
    jenkins.build_job(name, parameters={'tag': dep.version})
    sleep(30)
    console_output = jenkins.get_build_console_output(name, number)
    dep.console_output = console_output
    dep.save()
    return '[{}] Project release completed.......'.format(dep.webname.name)

@app.task(name="sendmail")
def mail(id,appli="",revie="",statu=0):
    alink = "http://localhost:8080/list"
    conlist = {
        0: ["发布申请",f"你有来自申请人{ appli }的发布申请ID { id }<br><a>{ alink }</a>",revie],
        1: ["上线申请",f"你有来自申请人{ appli }的上线申请ID { id }<br><a>{ alink }</a>",revie],
        2: ["已上线",f"你的发布申请ID { id }的已上线<br><a>{ alink }</a>",revie],
        3: ["已取消",f"你的发布申请ID { id }的已取消<br><a>{ alink }</a>",revie]
    }
    try:
        email = EmailMessage(conlist[statu][0], conlist[statu][1], to=[conlist[statu][2]])
        email.content_subtype = 'html'
        email.send()
    except Exception as e:
        print(e)
        traceback.print_exc()

