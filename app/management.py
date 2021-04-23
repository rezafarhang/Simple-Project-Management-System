from flask import Blueprint, request
from flask_login import login_required, current_user
from . import db
from .models import Board, BoardUser, BoardCard
import json

manage = Blueprint('manage', __name__)


@manage.route('/profile', methods=['GET'])
@login_required
def profile_preview():
    user_name = current_user.fullname
    user_email = current_user.email
    return json.dumps(
        {
            'status_code': '200',
            'fullname': user_name,
            'email': user_email
        }
    )


@manage.route('/profile/delete', methods=['POST'])
@login_required
def delete_account():
    db.session.delete(current_user)
    user_id = current_user.id
    db.session.delete(user_id)

    return json.dumps(
        {
            'status_code': '200',
            'message': 'Account Deleted Sucessfully'
        }
    )


@manage.route('/boards', methods=['GET'])
@login_required
def show_boards():
    user_board_ids = BoardUser.query.filter_by(user_id=current_user.id).all()
    for id in user_board_ids:
        user_board_names = Board.query.get(id).board_name

    if user_board_names.empty():
        return json.dumps(
            {
                'status_code': '204',
                'message': 'No Board Found'
            }
        )

    return json.dumps(
        {
            'status_code': '200',
            'boards': user_board_names
        }
    )


@manage.route('/boards', methods=['POST'])
@login_required
def create_board():
    json_data = request.get_json()
    admin_id = current_user.id
    admin_name = current_user.fullname
    board_name = json_data.get('board_name')
    if not board_name:
        pass
    board = Board.query.filter_by(board_name=board_name).first()
    if board:
        return json.dumps(
            {
                'status_code': '403',
                'message': 'This Board Already Exist'
            }
        )

    db.session.add(
        Board(admin_id=admin_id,
              admin_name=admin_name,
              board_name=board_name)
    )
    db.Session.add(
        BoardUser(user_id=current_user.id)
    )
    db.session.commit()

    return json.dumps(
        {
            'status_code': '201',
            'message': 'Board Created Sucessfully'
        }
    )


@manage.route('/boards/remove', methods=['POST'])
@login_required
def delete_board():
    json_data = request.get_json()
    admin_id = current_user.id
    board_name = json_data.get('board_name')

    Board.query.filter_by(board_name=board_name, admin_id=admin_id).delete()
    BoardCard.query.filter_by(board_name=board_name).delete()
    db.session.commit()

    return json.dumps(
        {
            'status_code': '200',
            'message': 'Board Deleted Sucessfully'
        }
    )


@manage.route('/boards/edit', methods=['POST'])
@login_required
def edit_board():
    json_data = request.get_json()
    admin_id = current_user.id
    board_name = json_data.get('board_name')

    board = Board.query.filter_by(board_name=board_name, admin_id=admin_id)
    board_new_name = json_data.get('board_new_name')
    if not board_new_name:
        return json.dumps(
            {
                'status_code': '404',
                'message': 'No New Name Found'
            }
        )

    board.board_name = board_new_name
    db.session.commit()
    return json.dumps(
        {
            'status_code': '200',
            'message': 'Board Name Edited Sucessfully'
        }
    )


@manage.route('/card/add', methods=['POST'])
@login_required
def create_card():
    json_data = request.get_json()
    card_name = json_data.get('card_name')
    card_field = json_data.get('card_field')
    board_name = json_data.get('board_name')
    board_id = Board.query().filter_by(board_name=board_name).first().id

    db.session.add(
        BoardCard(card_name=card_name,
                  card_field=card_field,
                  board_id=board_id)
    )
    db.session.commit()

    return json.dumps(
        {
            'status_code': '201',
            'message': 'Board Created Sucessfully'
        }
    )


@manage.route('/card/remove', methods=['POST'])
@login_required
def delete_card():
    json_data = request.get_json()
    card_name = json_data.get('card_name')
    board_name = json_data.get('board_name')
    board_id = Board.query().filter_by(board_name=board_name).first().id

    BoardCard.qurey.filter_by(card_name=card_name, board_id=board_id).delete()
    db.session.commit()

    return json.dumps(
        {
            'status_code': '204',
            'message': 'Card Deleted Sucessfully'
        }
    )


@manage.route('/card/edit', methods=['POST'])
@login_required
def edit_card():
    json_data = request.get_json()
    card_name = json_data.get('card_name')
    board_name = json_data.get('board_name')
    board_id = Board.query().filter_by(board_name=board_name).first().id

    card = BoardCard.qurey.filter_by(card_name=card_name, board_id=board_id)
    card_new_name = json_data.get('card_new_name')
    if not card_new_name:
        return json.dumps(
            {
                'status_code': '404',
                'message': 'No New Name Found'
            }
        )

    card.card_name = card_new_name
    return json.dumps(
        {
            'status_code': '200',
            'message': 'Card Edited Sucessfully'
        }
    )
