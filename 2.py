from flask import Flask, request, jsonify
from random import choice

app = Flask(__name__)

groups = {}
last_id = 0

class Group:
    def __init__(self, id, name, description, participants):
        self.id = id
        self.name = name
        self.description = description
        self.participants = participants

class Participant:
    def __init__(self, id, name, wish):
        self.id = id
        self.name = name
        self.wish = wish
        self.recipient = False
        self.ignoreid = -1

@app.route('/group', methods=['POST'])
def create_group():
    global last_id
    data = request.get_json()
    id = last_id + 1
    last_id += 1
    group = Group(id, data['name'], data['description'], [])
    groups[id] = group
    return jsonify(id=id), 201

@app.route('/groups', methods=['GET'])
def get_all_groups():
    response = [
        {
            'id': group.id,
            'name': group.name,
            'description': group.description
        }
        for group in groups.values()
    ]
    return jsonify(response), 200

@app.route('/group/<id>', methods=['GET'])
def get_group(id):
    id = int(id)
    if id not in groups:
        return jsonify({'error': 'Group not found'}), 404

    group = groups[id]
    
    participants = []
    for participant in group.participants:
        if participant.recipient != False:
            participants.append({'id': participant.id, 'name': participant.name, 'wish': participant.wish, 'recipient': {'id': participant.recipient.id, 'name': participant.recipient.name, 'wish': participant.recipient.wish}})
        else:
            participants.append({'id': participant.id, 'name': participant.name, 'wish': participant.wish, 'recipient': {}})

    response = {
        'id': group.id,
        'name': group.name,
        'description': group.description,
        'participants': participants
    }

    return jsonify(response), 200

@app.route('/group/<id>', methods=['PUT'])
def update_group(id):
    id = int(id)
    if id not in groups:
        return jsonify({'error': 'Group not found'}), 404

    data = request.get_json()
    group = groups[id]
    group.name = data['name']
    group.description = data['description']
    return jsonify(status='success'), 202

@app.route('/group/<id>', methods=['DELETE'])
def delete_group(id):
    id = int(id)
    if id not in groups:
        return jsonify({'error': 'Group not found'}), 404

    del groups[id]
    return jsonify(status='success'), 204

@app.route('/group/<id>/participant', methods=['POST'])
def add_participant(id):
    id = int(id)
    global last_id
    if id not in groups:
        return jsonify({'error': 'Group not found'}), 404

    data = request.get_json()
    participant_id = last_id + 1
    last_id += 1
    if 'wish' in data:        
        participant = Participant(participant_id, data['name'], data['wish'])
    else:
        participant = Participant(participant_id, data['name'], 'none')
    groups[id].participants.append(participant)
    return jsonify(id=participant_id), 201

@app.route('/group/<group_id>/participant/<participant_id>', methods=['DELETE'])
def remove_participant(group_id, participant_id):
    group_id = int(group_id)
    participant_id = int(participant_id)
    if group_id not in groups:
        return jsonify({'error': 'Groups not found'}), 404
    
    group = groups[group_id]
    participant = next((p for p in group.participants if p.id == participant_id), None)

    if participant is None:
        return jsonify({'error': 'Participant not found'}), 404

    group.participants.remove(participant)
    return jsonify(status='success'), 204

@app.route('/group/<id>/toss', methods=['POST'])
def do_toss(id):
    id = int(id)
    if id not in groups:
        return jsonify({'error': 'Group not found'}), 404
    if len(groups[id].participants) < 3:
        return jsonify({'error': 'Conflict'}), 409
    free_participants = []
    for participant in groups[id].participants:
        free_participants.append(participant)
    for participant in groups[id].participants:
        free_participants_without_santa = []
        for free_participant in free_participants:
            free_participants_without_santa.append(free_participant)
        if participant in free_participants_without_santa:
            free_participants_without_santa.remove(participant)
        participant_recipient = choice(free_participants_without_santa)
        if participant_recipient.recipient != False and participant_recipient.ignoreid == participant.id:
            free_participants_without_santa.remove(participant_recipient)
            participant_recipient = choice(free_participants_without_santa)
        participant.recipient = participant_recipient
        participant.ignoreid = participant_recipient.id
        free_participants.remove(participant_recipient)

    response = [
        {
            'id': participant.id,
            'name': participant.name,
            'wish': participant.wish,
            'recipient': {
                'id': participant.recipient.id,
                'name': participant.recipient.name,
                'wish': participant.recipient.wish,
            }
        }
        for participant in groups[id].participants
    ]
    return jsonify(response), 200

@app.route('/group/<groupId>/participant/<participantId>/recipient', methods=['GET'])
def get_recipient(groupId, participantId):
    groupId = int(groupId)
    participantId = int(participantId)
    if groupId not in groups:
        return jsonify({'error': 'Group not found'}), 404
    if not any(p.id == participantId for p in groups[groupId].participants):
        return jsonify({'error': 'Participant not found'}), 404
    for p in groups[groupId].participants:
        if p.id == participantId:
            rec = p.recipient
    if rec != False:
        response = {
            'id': rec.id,
            'name': rec.name,
            'wish': rec.wish,
        }
    else:
        response = {}

    return jsonify(response), 200

app.run(host='0.0.0.0', port=8080)