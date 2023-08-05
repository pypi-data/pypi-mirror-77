#include "Sound.h"

#include "soloud_wav.h"
#include "soloud_wavstream.h"
#include "soloud_sfxr.h"

Sound* Sound::instance;

Sound::Sound()
	:initialized(false)
	, m_soloud(nullptr)
{
	init();
}

Sound::~Sound()
{
	delete m_soloud;
}

void Sound::init()
{
	if (m_soloud == nullptr)
	{
		m_soloud = new SoLoud::Soloud();
		m_soloud->init();		
	}
	initialized = true;
}

void Sound::release()
{
	if (m_soloud != nullptr)
	{
		stopAllSound();
		releaseAllSound();

		m_soloud->deinit();

		delete m_soloud;
		m_soloud = nullptr;
	}
	initialized = false;
}

void Sound::update()
{
	m_soloud->update3dAudio();
}

void Sound::load(const char* filename, bool stream)
{
	auto it = m_audioSourcesDict.find(filename);
	if (it == m_audioSourcesDict.end())
	{
		if (stream)
		{
			WavStream* audio = new WavStream();
			audio->load(filename);
			m_audioSourcesDict[filename] = audio;
		}
		else
		{
			Wav* audio = new Wav();
			audio->load(filename);
			m_audioSourcesDict[filename] = audio;
		}
	}
}

void Sound::unload(const char* filename)
{
	auto it = m_audioSourcesDict.find(filename);
	if (it != m_audioSourcesDict.end())
	{
		it->second->stop();
		delete it->second;
		m_audioSourcesDict.erase(it);
	}
}

void Sound::fadeVolume(int handle, float aTo, float aTime)
{
	m_soloud->fadeVolume(handle, aTo, aTime);
}

void Sound::scheduleStop(int handle, float aTime)
{
	m_soloud->scheduleStop(handle, aTime);
}

void Sound::setGlobalVolume(float volume)
{
	m_soloud->setGlobalVolume(volume);
}

float Sound::getGlobalVolume()
{
	return m_soloud->getGlobalVolume();
}

double Sound::getStreamTime(int handle)
{
	return m_soloud->getStreamTime(handle);
}

int Sound::play(const char* filename, bool stream, bool loop, bool is_3d, float x, float y, float z, float volume)
{
	if (!isInitialized())
	{
		LOG("Sound need to initialize first");
		return 0;
	}

	auto it = m_audioSourcesDict.find(filename);
	if (it != m_audioSourcesDict.end())
	{
		it->second->setLooping(loop);
		return m_soloud->play(*it->second, volume);
	}
	else
	{
		if(stream)
		{
			WavStream* audio = new WavStream();
			audio->setSingleInstance(true);
			audio->load(filename);
			audio->setLooping(loop);
			m_audioSourcesDict[filename] = audio;
			return m_soloud->play(*audio, volume);			
		}
		else
		{
			Wav* audio = new Wav();
			audio->load(filename);
			audio->setLooping(loop);
			m_audioSourcesDict[filename] = audio;

			if (is_3d)
			{
				audio->set3dMinMaxDistance(1, 200);
				audio->set3dAttenuation(AudioSource::EXPONENTIAL_DISTANCE, 0.25);
				return m_soloud->play3d(*audio, x, y, z, 0.0, 0.0, 0.0, volume);
			}

			return m_soloud->play(*audio, volume);
		}		
	}
}

void Sound::stop(const char* filename)
{
	auto it = m_audioSourcesDict.find(filename);
	if (it != m_audioSourcesDict.end())
	{
		Wav* audio = (Wav*)(it->second);
		m_soloud->stopAudioSource(*audio);
	}
}

void Sound::stop(int handle)
{
	m_soloud->stop(handle);
}

void Sound::stopAllSound()
{
	m_soloud->stopAll();
}

void Sound::releaseAllSound()
{
	for (auto it = m_audioSourcesDict.begin(); it != m_audioSourcesDict.end(); it++)
	{
		it->second->stop();
		delete (it->second);
	}

	m_audioSourcesDict.clear();
}

int Sound::playPreset(int sfx_preset, bool is_loop, bool is_3d, float x, float y, float z, float volume)
{
	if (!isInitialized())
	{
		LOG("Sound need to initialize first");
		return 0;
	}

	char filename[64];
	sprintf(filename, "sfxr_%d", sfx_preset);

	auto it = m_audioSourcesDict.find(filename);
	if (it != m_audioSourcesDict.end())
	{
		if (is_3d)
		{
			it->second->setLooping(is_loop);
			it->second->set3dMinMaxDistance(1, 200);
			it->second->set3dAttenuation(AudioSource::EXPONENTIAL_DISTANCE, 0.25);
			return m_soloud->play3d(*it->second, x, y, z, 0.0, 0.0, 0.0, volume);
		}
		return m_soloud->play(*it->second, volume);
	}
	else
	{		
		Sfxr* audio = new Sfxr();
		audio->loadPreset(sfx_preset, 3);
		m_audioSourcesDict[filename] = audio;
		if (is_3d)
		{
			audio->setLooping(is_loop);
			audio->set3dMinMaxDistance(1, 200);
			audio->set3dAttenuation(AudioSource::EXPONENTIAL_DISTANCE, 0.25);
			return m_soloud->play3d(*audio, x, y, z, 0.0, 0.0, 0.0, volume);
		}
		return m_soloud->play(*audio, volume);
	}
}

void Sound::set3dSourcePosition(int handle, float x, float y, float z)
{
	m_soloud->set3dSourcePosition(handle, x, y, z);
}

void Sound::set3dMinMaxDistance(int handle, float min, float max)
{
	m_soloud->set3dSourceMinMaxDistance(handle, min, max);
}

void Sound::set3dAttenuation(int handle, int attenuationModel, float rolloffFactor)
{
	m_soloud->set3dSourceAttenuation(handle, attenuationModel, rolloffFactor);
}