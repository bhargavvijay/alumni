from flask import Blueprint, render_template, request, flash, jsonify, session, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
from .models import User, Company_User, Job, JobApplied
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def firstpage():
    return render_template("first page.html", user=current_user)


@views.route('/alumnihome', methods=['GET', 'POST'])
@login_required
def alumnihome():
    return render_template("alumnihome.html", user=current_user)

@views.route('/apply_job/<int:job_id>', methods=['POST'])
@login_required
def apply_job(job_id):
    # Retrieve the job and user
    job = Job.query.get(job_id)
    user = current_user

    # Create a new job application entry
    new_application = JobApplied(job_id=job_id, user_id=user.id)
    db.session.add(new_application)
    db.session.commit()
    for job in session['jobs_available']:
        if job['id'] == job_id:
            job['applied'] = True
    flash('Application submitted successfully!', category='success')
    return redirect(url_for('views.jobsavailable'))

@views.route('/jobsavailable', methods=['GET', 'POST'])
@login_required
def jobsavailable():
    jobs_available=session['jobs_available']
    user=current_user
    return render_template('jobsavailable.html',user=current_user,jobs_available=jobs_available)


@views.route('/searchjob', methods=['GET', 'POST'])
@login_required
def searchjob():
    if request.method == 'POST':
        search_according_qualification = request.form.get('search_according_qualification')
        all_jobs = Job.query.all()
        all_companies = Company_User.query.all()
        jobs_according_to_search = []

        user_applied_jobs = []
        user=current_user
        all_job_applications=JobApplied.query.all()
        for job_application in all_job_applications:
            if job_application.user_id==user.id:
                user_applied_jobs.append(job_application.job_id)

        i = 1
        for jobs in all_jobs:
            if jobs.qualifications_required == search_according_qualification:
                company_name = None
                for company in all_companies:
                    if company.id == jobs.company__user_id:
                        company_name = company.company_name
                        break
                job_info = {
                    'sl_no': i,
                    'id':jobs.id,
                    'job_title': jobs.title,
                    'qualifications_required': jobs.qualifications_required,
                    'additional_requirements': jobs.additional_requirements,
                    'company_name': company_name,
                    'applied': jobs.id in user_applied_jobs  # Check if user has applied
                }
                jobs_according_to_search.append(job_info)
                i += 1

        session['jobs_available'] = jobs_according_to_search
        return redirect(url_for('views.jobsavailable'))
    return render_template('searchjob.html', user=current_user)



@views.route('/addjob', methods=['POST', 'GET'])
@login_required
def addjob():
    if request.method == 'POST':
        job_title = request.form.get('jobtitle')
        qualifications_required = request.form.get('qualifications_required')
        print(qualifications_required)
        job_additional_requirments = request.form.get('additionalrequirments')
        company_id = session['id']
        new_job = Job(title=job_title, qualifications_required=qualifications_required,
                      additional_requirements=job_additional_requirments, company__user_id=company_id)
        db.session.add(new_job)
        db.session.commit()
        flash('Job was added successfully', category='success')
        return redirect('/addjob')
    return render_template("addjob.html", user=current_user)


@views.route('/companyhome', methods=['GET', 'POST'])
@login_required
def companyhome():
    return render_template("companyhome.html", user=current_user)



