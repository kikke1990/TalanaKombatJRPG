from django.db import models

class Movement(models.Model):
    mov_id = models.AutoField(primary_key=True)
    mov_nmonico = models.CharField(max_length=1)
    mov_name = models.TextField()
    class Meta:
        managed = True
        db_table = 'movement'

    def __str__(self) -> str:
        if self.mov_nmonico == 'S':
            return ' se agacha'
        if self.mov_nmonico == 'W':
            return ' salta'
        return f' se mueve hacia la {self.mov_name}'

class Blow(models.Model):
    blw_id = models.AutoField(primary_key=True)
    blw_nmonico = models.CharField(max_length=1)
    blw_name = models.TextField()
    class Meta:
        managed = True
        db_table = 'blow'

    def __str__(self):
        if self.blw_nmonico == 'P':
            return f''' da un {self.blw_name}'''
        return f''' da una {self.blw_name}'''

class SpecialBlow(models.Model):
    sbw_id = models.AutoField(primary_key=True)
    sbw_name = models.TextField()
    sbw_combination = models.TextField()
    class Meta:
        managed = True
        db_table = 'special_blow'

class Player(models.Model):
    ply_id = models.AutoField(primary_key=True)
    ply_nombre = models.TextField()
    ply_life_point = models.IntegerField(blank=True,null=True)
    class Meta:
        managed = True
        db_table = 'player'
    
    def __str__(self) -> str:
        return self.ply_nombre

class PlayerSpecialBlow(models.Model):
    psb_id = models.AutoField(primary_key=True)
    ply = models.ForeignKey(Player,on_delete=models.CASCADE)
    sbw = models.ForeignKey(SpecialBlow,on_delete=models.CASCADE)
    class Meta:
        managed = True
        db_table = 'player_special_blow'

    def __str__(self) -> str:
        return f'{self.ply.ply_nombre} conecta un {self.sbw.sbw_name}'

class Damage(models.Model):
    dmg_id = models.AutoField(primary_key=True)
    dmg_ind_special = models.BooleanField(default=False)
    dmg_point = models.IntegerField()
    blw_id = models.ForeignKey(Blow,on_delete=models.CASCADE,blank=True,null=True)
    sbw_id = models.ForeignKey(SpecialBlow,on_delete=models.CASCADE,blank=True,null=True)
    class Meta:
        managed = True
        db_table = 'damage'

class Game(models.Model):
    gam_id = models.AutoField(primary_key=True)
    gam_datetime = models.DateTimeField(auto_now=True)
    ply_wing = models.ForeignKey(Player,on_delete=models.CASCADE,blank=True,null=True)
    class Meta:
        managed = True
        db_table = 'game'
        
    def __str__(self):
        return self.gam_datetime.strftime("%d/%m/%Y %H:%M:%S")

class EventGame(models.Model):
    evg_id = models.AutoField(primary_key=True)
    gam_id = models.ForeignKey(Game,on_delete=models.CASCADE,blank=True,null=True,related_name='event_games')
    evg_descripcion = models.TextField()
    class Meta:
        managed = True
        db_table = 'event_game'