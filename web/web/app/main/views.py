from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm , TypeForm
from .. import db
from ..models import Role, User, Tag, Type, Video, Comment
from ..decorators import admin_required


@main.route('/', methods=['GET', 'POST'])
def index():
    form = TypeForm()
    temp_type = '全部'
    if form.validate_on_submit():
        temp_type = form.type.data;
        print(form.type.data)
    else:
        print(form.errors)
    page = request.args.get('page', 1, type=int)
    if temp_type == '全部':
        pagination =Video.query.order_by(Video.id.desc()).paginate(
            page, per_page=20,
            error_out=False)
    else:
        type = Type.query.filter_by(name=temp_type).first_or_404()
        pagination = type.videos.paginate(
            page, per_page=20,
            error_out=False)
    videos = pagination.items
    return render_template('index.html', videos=videos,pagination=pagination,form = form)

@main.route('/video/<id>')
def video(id):
    # vvido = Video.query.get_or_404(id)
    # print(vvido.name)
    # print(vvido.introduce)
    # commmet = vvido.comments.all()
    # print(commmet[0].body)
    # userr = commmet[0].author
    # print(userr.username)
    # tyype = vvido.types.all()
    # print(tyype[0].name)
    # tagg = vvido.tags.all()
    # print(tagg[0].name)
    # print(tagg[1].name)
    video = Video.query.get_or_404(id)
    return render_template('video.html',video=video,comments=video.comments )


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.birth = form.birthday.data
        current_user.location = form.location.data
        current_user.interests = form.interests.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('您的个人信息已被更新。')
        return redirect(url_for('.user', username=current_user.username))
    form.birthday.data = current_user.birth
    form.location.data = current_user.location
    form.interests.data = current_user.interests
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
