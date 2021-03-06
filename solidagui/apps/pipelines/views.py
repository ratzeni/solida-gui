from django.views.generic.base import TemplateView
from components.pipelines import Pipelines, Pipeline
from django.conf import settings

from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader, RequestContext

import json


class BrowseView(TemplateView):
    template_name = 'pipelines/browse.html'

    def get_pipelines_layout(self, pipelines, n=2):
        it = [iter(pipelines)] * n
        layout = list(zip(*it))
        mod = len(pipelines) % n
        if mod != 0:
            layout.append(pipelines[-mod:])
        return layout

    def get_context_data(self, **kwargs):
        context = super(BrowseView, self).get_context_data(**kwargs)
        context['pipelines'] = self.get_pipelines_layout(Pipelines().pipelines)
        return context


def refresh():
    Pipelines().refresh_pipelines()
    return redirect('/pipelines/browse/')


def add_new(request):
    params = request.POST.dict()
    if not params.get('to_do'):
        template = loader.get_template('pipelines/add_new.html')
        context = dict()
        return HttpResponse(template.render(context, request))
    else:

        pipeline_dict = dict(
            label=params.get('label'),
            url=params.get('url'),
            description=params.get('description'),
            vars=json.loads(params.get('custom_vars'))
        )
        Pipelines().add_new_pipeline(pipeline_dict=pipeline_dict)
        return redirect('/pipelines/{}/setup/'.format(pipeline_dict.get('label')))


def setup(request, pipeline_id):
    template = loader.get_template('pipelines/setup.html')

    pipeline = Pipeline(pipeline_id=pipeline_id, with_profiles=True)
    to_do = request.POST.dict().get("to_do")

    if to_do and 'load' in to_do:
        profile_id = request.POST.dict().get("profile_selected")
    elif to_do and 'save' in to_do:
        profile_id = request.POST.dict().get("profile_name")
        pipeline.create_profile(profile_id, request.POST.dict())
    else:
        profile_id = None

    context = dict(pipeline=pipeline,
                   profile=pipeline.get_profile(profile_id=profile_id if profile_id else settings.SOLIDA_PROFILE_NAME),
                   profile_id=profile_id,
                   sample_profile=settings.SOLIDA_PROFILE_NAME,
                   deployment_modes=settings.SOLIDA_DEPLOY_MODES,
                   project_dir=settings.SOLIDA_PROJECTS_PATH,
                   tmp_dir=settings.SOLIDA_TMP_PATH,
                   )

    return HttpResponse(template.render(context, request))


def deploy(request, pipeline_id):

    def retrieve_result(result):
        return dict(
            stdout_data=result.get('stdout_data').decode().split('\n') if result.get('stdout_data') else None,
            stderr_data=result.get('stderr_data').decode().split('\n') if result.get('stderr_data') else None,
            exit_code=int(result.get('exit_code')),
            success=True if result.get('stdout_data') and 'failed=0' in result.get('stdout_data').decode() and
                            'unreachable=1' not in result.get('stdout_data').decode() else False,
            last_row=result.get('stdout_data').decode().split('\n')[-5]
        )

    template = loader.get_template('pipelines/deploy.html')

    profile_id = request.POST.dict().get("profile_name")
    pipeline = Pipeline(pipeline_id=pipeline_id, with_profiles=True)
    pipeline.create_profile(profile_id, request.POST.dict())
    profile = pipeline.get_profile(profile_id=profile_id)
    result = profile.deploy()
    context = dict(pipeline=pipeline,
                   profile=profile,
                   result=retrieve_result(result))

    return HttpResponse(template.render(context, request))




