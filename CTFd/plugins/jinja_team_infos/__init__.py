from CTFd.utils.user import get_current_user
from CTFd.models import Teams

def load(app):
    app.jinja_env.globals['getTeamPlace']=getTeamPlace
    app.jinja_env.globals['getTeamPoints']=getTeamPoints
    app.jinja_env.globals['getTeamName']=getTeamName


def getTeamPlace():
    user = get_current_user()
    # print(f'user: <{user}>===========================================')
    if not user:
        return None
    # print(f'user.team_id: <{user.team_id}>===========================================')
    
    if not user.team_id:
        return None
    
    team_id = user.team_id
    team = Teams.query.filter_by(id=team_id).first()

    place = team.place
    if not place:
        return None

    return f"{place}"

def getTeamPoints():
    user = get_current_user()
    # print(f'user: <{user}>===========================================')
    if not user:
        return None
    # print(f'user.team_id: <{user.team_id}>===========================================')
    
    if not user.team_id:
        return None
    
    team_id = user.team_id
    team = Teams.query.filter_by(id=team_id).first()

    score = team.get_score(admin=True)
    if not score:
        return None

    return f"{score}"

def getTeamName():
    user = get_current_user()
    # print(f'user: <{user}>===========================================')
    if not user:
        return None
    # print(f'user.team_id: <{user.team_id}>===========================================')
    
    if not user.team_id:
        return None
    
    team_id = user.team_id
    team = Teams.query.filter_by(id=team_id).first()

    name = team.name
    if not name:
        return None

    return f"{name}"