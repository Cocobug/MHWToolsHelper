listc=["CoalescenceII","OffensiveGuardIII","EffluviaExpertI","SpreadPowerShotsII","RazorSharpSpareShotI","SurveyorsScoutflyI","ParaFunctionalityI","AdamantineI","CriticalBoostII","PoisonResistanceIII","AttackBoostIV","DefenseBoostV","ParalysisResistanceIII","SleepResistanceIII","StunResistanceIII","WindproofIV","HealthBoostIII","RecoveryUpIII","FireResistanceIII","WaterResistanceIII","ThunderResistanceIII","FireAttackV","WaterAttackIV","ThunderAttackV","PoisonAttackIV","ParalysisAttackIV","SleepAttackIV","SluggerIII","StaminaThiefIII","ArtilleryIII","HungerResistanceIII","GuardV","WideRangeV","ItemProlongerIII","SpeedEatingIII","DivineBlessingIII","PalicoRallyV","BotanistIV","GeologistIII","SlingerCapacityIII","StealthIII","SporepuffExpertIII","AquaticExpertIII","EntomologistIII","IntimidatorIII","HeavyArtilleryII","FreeMealI","ScentHoundI","FortifyI","HornMaestroII","CapacityBoostI","BleedingResistanceIII","RecoverySpeedIII","IceResistanceIII","BlightResistanceIII","IceAttackV","CriticalEyeIV","EvadeWindowIV","QuickSheathIII","SpeedSharpeningIII","BlastResistanceIII","DragonResistanceIII","DragonAttackIII","BlastAttackIV","CriticalDrawII","SpecialAmmoBoostII","MarathonRunnerIII","ConstitutionIV","StaminaSurgeII","EvadeExtenderII","BombardierIII","MushroomancerII","FreeElementIII","HandicraftIV","MudPuppyI","TrickshotI","HunterLifeI","ProcurerI","GathererI","EarplugsIV","TremorResistanceIII","WeaknessExploitII","FocusIII","PartbreakerIII","ResentmentIV","HeroicsIV","ToolSpecialistIII","LatentPowerII","AgitatorIV","PeakPerformanceII","MaximumMightII","FlinchFreeIII","EffluviaResistanceIII","NormalShotsII","ClearmindI","RiderI","SurveyorI","PiercingShotsII","SpreadShotsI","PoisonFuncI","ParaFuncI","SleepFuncI","BlastFuncI","GeomancyI","GaleI","WyrmslayerI","BulwarkI","FairWindI","PowerProlongerIII"]

for c in listc:
    with open("C:/MAMP/htdocs/MHWTools/armorcalc/armors/CH/"+c+".js") as f:
        print(f.read()[1:-2]+",")
