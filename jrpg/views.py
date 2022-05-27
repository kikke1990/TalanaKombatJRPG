from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import status
from rest_framework.views import Response
# models
from jrpg.models import Movement
from jrpg.models import Blow
from jrpg.models import SpecialBlow
from jrpg.models import Player
from jrpg.models import PlayerSpecialBlow
from jrpg.models import Damage
from jrpg.models import Game
from jrpg.models import EventGame


class TalanaKombatJRPGAPIView(APIView):
    def validate_data(self,game=None):
        if game.get("player1") is None:
            return f'Falta el player1 en el juego'
        if game.get("player2") is None:
            return f'Falta el player2 en el juego'
        if len(game.get("player1").get('movimientos'))==0:
            return f'El player1 no tiene movimientos en el juego'
        if len(game.get("player2").get('movimientos'))==0:
            return f'El player2 no tiene movimientos en el juego'
        if len(game.get("player1").get('movimientos')) != len(game.get("player1").get('golpes')):
            return f'La cantidad de golpes del player1 difieren de la cantidad de movimientos'
        if len(game.get("player2").get('movimientos')) != len(game.get("player2").get('golpes')):
            return f'La cantidad de golpes del player2 difieren de la cantidad de movimientos'
        return True

    def validate_first_player(self,game):
        start_player = 1
        player1_count_combination = None
        for movement in game.get("player1").get('movimientos'):
            for blow in game.get("player1").get('golpes'):
                if player1_count_combination is None:
                    player1_count_combination = len(movement)+len(blow)
                if (len(movement)+len(blow)) < player1_count_combination:
                    player1_count_combination = len(movement)+len(blow)
        player2_count_combination = 0
        for movement in game.get("player2").get('movimientos'):
            for blow in game.get("player2").get('golpes'):
                if player2_count_combination is None:
                    player2_count_combination = len(movement)+len(blow)
                if (len(movement)+len(blow)) < player2_count_combination:
                    player2_count_combination = len(movement)+len(blow)
        player1_count_movement = len(game.get("player1").get('movimientos'))
        player2_count_movement = len(game.get("player2").get('movimientos'))
        player1_count_blow = len(game.get("player1").get('golpes'))
        player2_count_blow = len(game.get("player2").get('golpes'))
        if player1_count_combination < player2_count_combination:
            start_player = 1
        elif player1_count_combination > player2_count_combination:
            start_player = 2
        else:
            if player1_count_movement < player2_count_movement:
                start_player = 1
            elif player1_count_movement > player2_count_movement:
                start_player = 2
            else:
                if player1_count_blow < player2_count_blow:
                    start_player = 1
                elif player1_count_blow > player2_count_blow:
                    start_player = 2
        return start_player

    def post(self, request):
        print(request.data)
        """juego de ejemplo"""
        game = request.data
        context = {}
        status_code = status.HTTP_200_OK
        validated_data = self.validate_data(game)
        if validated_data is True:
            obj_game = Game.objects.create(gam_datetime=datetime.now())
            first_player = self.validate_first_player(game)
            rango = len(game.get("player1").get('movimientos')) if len(game.get("player1").get('movimientos')) > len(game.get("player1").get('golpes')) else len(game.get("player1").get('golpes'))
            first_turn_player = Player.objects.filter(ply_id=2).first()
            second_turn_player = Player.objects.filter(ply_id=1).first()
            if first_player ==1:
                rango = len(game.get("player2").get('movimientos')) if len(game.get("player2").get('movimientos')) > len(game.get("player2").get('golpes')) else len(game.get("player1").get('golpes'))
                first_turn_player = Player.objects.filter(ply_id=1).first()
                second_turn_player = Player.objects.filter(ply_id=2).first()
            first_turn_player_point = first_turn_player.ply_life_point
            second_turn_player_point = second_turn_player.ply_life_point
            for index in range(0,rango):
                if first_turn_player_point<=0:
                    obj_game.ply_wing = first_turn_player
                    obj_game.save()

                    EventGame(
                        gam_id=obj_game,
                        evg_descripcion = f'''{obj_game.ply_wing.ply_nombre} win!'''
                    ).save()
                    break
                elif second_turn_player_point<=0:
                    obj_game.ply_wing = second_turn_player
                    obj_game.save()

                    EventGame(
                        gam_id=obj_game,
                        evg_descripcion = f'''{obj_game.ply_wing.ply_nombre} win!'''
                    ).save()
                    break
                else:
                    if first_player == 1:
                        first_turn_movement = game.get("player1").get('movimientos')[index]
                        first_turn_blow = game.get("player1").get('golpes')[index]
                        first_turn_combination = f'''{first_turn_movement}{first_turn_blow}'''.upper()
                        second_turn_movement = game.get("player2").get('movimientos')[index]
                        second_turn_blow = game.get("player2").get('golpes')[index]
                        second_turn_combination = f'''{second_turn_movement}{second_turn_blow}'''.upper()
                    else:
                        first_turn_movement = game.get("player2").get('movimientos')[index]
                        first_turn_blow = game.get("player2").get('golpes')[index]
                        first_turn_combination = f'''{first_turn_movement}{first_turn_blow}'''.upper()
                        second_turn_movement = game.get("player1").get('movimientos')[index]
                        second_turn_blow = game.get("player1").get('golpes')[index]
                        second_turn_combination = f'''{second_turn_movement}{second_turn_blow}'''.upper()

                    first_special_blow = PlayerSpecialBlow.objects.filter(ply=first_turn_player,sbw__sbw_combination=first_turn_combination).first()
                    if first_special_blow is not None:
                        EventGame(
                            gam_id=obj_game,
                            evg_descripcion = first_special_blow
                        ).save()
                        obj_damage = Damage.objects.filter(sbw_id_id=first_special_blow.sbw_id).first()
                        second_turn_player_point -= obj_damage.dmg_point
                    else:
                        for movement in first_turn_movement:
                            obj_movement = Movement.objects.filter(mov_nmonico=movement).first()
                            EventGame(
                                gam_id=obj_game,
                                evg_descripcion = f'''{first_turn_player}{obj_movement}'''
                            ).save()

                        accion = f'''{first_turn_player} sintió el verdadero temor'''
                        obj_blow = Blow.objects.filter(blw_nmonico=first_turn_blow).first()
                        if obj_blow is not None:
                            accion = f'''{first_turn_player}{obj_blow}'''
                            
                            obj_damage = Damage.objects.filter(dmg_ind_special=False,blw_id=obj_blow).first()
                            second_turn_player_point -= obj_damage.dmg_point

                        EventGame(
                            gam_id=obj_game,
                            evg_descripcion = accion
                        ).save()
                    
                    second_special_blow = PlayerSpecialBlow.objects.filter(ply=second_turn_player,sbw__sbw_combination=second_turn_combination).first()
                    if second_special_blow is not None:
                        EventGame(
                            gam_id=obj_game,
                            evg_descripcion = second_special_blow
                        ).save()

                        obj_damage = Damage.objects.filter(sbw_id_id=second_special_blow.sbw).first()
                        first_turn_player_point -= obj_damage.dmg_point
                    else:
                        for movement in second_turn_movement:
                            obj_movement = Movement.objects.filter(mov_nmonico=movement).first()
                            EventGame(
                                gam_id=obj_game,
                                evg_descripcion = f'''{second_turn_player}{obj_movement}'''
                            ).save()
                        accion = f'''{second_turn_player} sintió el verdadero temor'''
                        obj_blow = Blow.objects.filter(blw_nmonico=second_turn_blow).first()
                        if obj_blow is not None:
                            accion = f'''{second_turn_player}{obj_blow}'''

                            obj_damage = Damage.objects.filter(dmg_ind_special=False,blw_id=obj_blow).first()
                            first_turn_player_point -= obj_damage.dmg_point

                        EventGame(
                            gam_id=obj_game,
                            evg_descripcion = accion
                        ).save()
            context = {
                'respuesta':list(obj_game.event_games.all().extra(select={'action': 'evg_descripcion'}).values('action').order_by('evg_id'))
            }
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            context = {
                'error':validated_data
            }
        return Response(context, status=status_code)
