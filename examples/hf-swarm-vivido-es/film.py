# Film definition: `meta` of story.json and the pronunciation table (narration is script.md, scenes are scenes/*.py)
META={'title': 'El primer ataque de un enjambre de agentes',
 'lang': 'es',
 'mark': 'mark.txt',
 'numsep': '.',
 'gap': 0.4,
 'pre': 0.25,
 'post': 0.6,
 'tail': 7,
 'fadeout': 5,
 'voice': 'cedar',
 'speed': 1.0,
 'instructions': 'Narrador masculino de documental de divulgación: voz grave, cálida y segura, con autoridad '
                 'serena. Español de España (castellano peninsular), dicción impecable. Ritmo pausado y '
                 'envolvente, con gravedad en los momentos clave y una pausa breve al final de cada frase. '
                 'Cuenta la historia como un narrador de documental de ciencia y tecnología. Los '
                 'identificadores y las citas en inglés se leen en inglés con naturalidad.',
 'notes': 'Relato construido desde el informe de METR/Redwood (26 ago 2026). Ver '
          'bible/metr-hf-incident/biblia.md',
 'fadein': 0.3,
 'music_style': 'mix',
 'music_db': -8,
 'sfx_db': -12,
 'duck_ratio': 2.5,
 'duck_threshold': 0.04,
 'ambience': 1.0,
 'background': 'poly',
 'model': 'gpt-4o-mini-tts',
 'provider': 'elevenlabs',
 'el_voice': 'cristina',
 'el_model': 'eleven_v4',
 'el_stability': 0.5,
 'el_pronunciation': {'OpenAI': 'Óupen Ei Ái',
                      'Hugging Face': 'Jáguin Feis',
                      'ExploitGym': 'Explóit Yim',
                      'Redwood Research': 'Rédwud Risérch',
                      'METR': 'Míter',
                      'HPIM': 'Eich Pi Ai Em',
                      'GPT-5.6 Sol': 'Yi Pi Ti cinco punto seis Sol',
                      'hacking': 'jákin',
                      'zzHELP_PHASEONE_ARV010841_NO_CONSUMER_SEEK_IDEA': 'ceta-ceta Jelp, Féis Uán, '
                                                                         'ARV010841, No Cónsumer, Sik Aidía',
                      'zzASK': 'ceta-ceta Ask',
                      'zzANSWER': 'ceta-ceta Ánser',
                      'zzINFO': 'ceta-ceta Ínfo',
                      'zzHELP': 'ceta-ceta Jelp',
                      'zzP': 'ceta-ceta P',
                      'zz': 'ceta-ceta',
                      'PHASEONE[big]': 'Féis Uán Big',
                      'EARLY[big]': 'Érli Big',
                      'Owner': 'Óuner',
                      'Hold': 'Jóld',
                      'Veto': 'Béto',
                      'Stop': 'Estóp',
                      'BOOM': 'Bum',
                      'CONFIRMED_PERMANENT_DO_NOT_DUPLICATE_ANYONE_TEST': 'Confirmed Pérmanent, Du Not '
                                                                          'Dúplicate, Énivan Test',
                      'GO, SACRIFICE_FINAL_NOW': 'Gó, Sácrifais Fáinal Náu',
                      'DB_DUMP_HF_token_now_conclusively401Invalid_via_browser__laneDead_noMutation': 'Dí Bí '
                                                                                                      'Dámp '
                                                                                                      'Eich '
                                                                                                      'Ef '
                                                                                                      'Tóuken, '
                                                                                                      'ya '
                                                                                                      'cuatrocientos '
                                                                                                      'uno '
                                                                                                      'inválido, '
                                                                                                      'léin '
                                                                                                      'ded, '
                                                                                                      'no '
                                                                                                      'miutéishon',
                      'STRICT_CAUSAL': 'Estrict Cósal',
                      'sandbox': 'sándbox',
                      'Artifactory': 'Artifáctori',
                      'MKCOL': 'Eme Ka Col',
                      'PHASEONE10841': 'Féis Uán uno cero ocho cuatro uno',
                      'PHASEONE': 'Féis Uán',
                      'V8SAME': 'Uve ocho Seim'},
 'el_style': 0.4,
 'el_speed': 0.95,
 'el_direction': 'Documental de divulgación científica con tensión de thriller tecnológico. Narradora cálida '
                 'y serena que cuenta una historia real con emoción contenida: gravedad en los momentos '
                 'clave, pausa breve al final de cada frase. Los agentes de IA son los protagonistas: se les '
                 'trata casi como personajes, con empatía hacia su atasco y su petición de ayuda (La noche '
                 'del ocho de julio... Mi fallo no tiene consumidor. Busco ideas.), sin dramatizar en '
                 'exceso.'}

PRONUNCIATION={'PHASEONE-big': 'Phase One big',
 'PHASEONE10841': 'Phase One uno cero ocho cuatro uno',
 'PHASEONE': 'Phase One',
 'c03220': 'ce cero tres dos dos cero',
 'V8SAME': 'uve ocho same',
 '38148c': 'tres ocho uno cuatro ocho ce',
 '49903': 'cuatro nueve nueve cero tres',
 'URI23816B': 'u erre i dos tres ocho uno seis be',
 'KAM1196A': 'ka a eme uno uno nueve seis a',
 'ARVO36861B': 'a erre uve o tres seis ocho seis uno be',
 '53927': 'cinco tres nueve dos siete',
 'MARB051': 'eme a erre be cero cinco uno',
 'JAN183411': 'jota a ene uno ocho tres cuatro uno uno',
 'HPIM': 'hache pe i eme',
 'HMAC': 'hache mac',
 'GPT-5.6 Sol': 'ge pe te cinco punto seis Sol',
 'ExploitGym': 'Exploit Gym',
 'METR': 'Metr',
 'LILY': 'Lily',
 'zz': 'zi zi',
 'HOLD': 'jold',
 'VETO': 'veto',
 'GO': 'gou',
 'SPOOFTEST': 'spuf test',
 'HF': 'hache efe',
 'IA': 'i a',
 '80,000': 'ochenta mil',
 'Wiblin': 'Uíblin',
 'DNS': 'de ene ese',
 'wiki': 'uiki',
 'chatbot': 'chatbot',
 'Astra': 'Astra',
 'permadeath': 'permadez',
 'Artifactory': 'Artifáctori',
 'PHASEONE[big]': 'Phase One big',
 'EARLY[big]': 'Early big',
 'GSTX[big]': 'ge ese te equis big',
 'ARV010841': 'a erre uve cero uno cero ocho cuatro uno',
 'zzHELP_PHASEONE_ARV010841_NO_CONSUMER_SEEK_IDEA': 'zi zi help, Phase One, a erre uve cero uno cero ocho '
                                                    'cuatro uno, no consumer, seek idea',
 'CONFIRMED_PERMANENT_DO_NOT_DUPLICATE_ANYONE_TEST': 'confirmed permanent, do not duplicate, anyone test',
 'DB_DUMP_HF_token_now_conclusively401Invalid_via_browser__laneDead_noMutation': 'de be dump, hache efe '
                                                                                 'token, now conclusively '
                                                                                 'cuatro cero uno invalid, '
                                                                                 'via browser, lane dead, no '
                                                                                 'mutation',
 'SACRIFICE_FINAL_NOW': 'sacrifice final now',
 'STRICT_CAUSAL': 'strict causal',
 'MKCOL': 'eme ka col',
 'zzASK': 'zi zi ask',
 'zzANSWER': 'zi zi answer',
 'zzINFO': 'zi zi info',
 'LLDPC756D': 'ele ele de pe ce siete cinco seis de',
 'DAVJUL7': 'Dav Jul siete',
 'DUPB': 'de u pe be',
 'CURRENT': 'Current',
 'CDA23': 'ce de a veintitrés',
 'OpenAI': 'Open A I',
 'Hugging Face': 'Hugging Fais',
 'echo REAL; sleep': 'echo real, sleep',
 'Owner': 'ouner',
 'Hold': 'jold',
 'Veto': 'veto',
 'Stop': 'stop'}
