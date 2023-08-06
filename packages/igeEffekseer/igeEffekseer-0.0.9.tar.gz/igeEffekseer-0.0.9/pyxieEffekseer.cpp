
#if defined _WIN32
#   include <glew.h>
#   include <gl/gl.h>
#   include <gl/glu.h>
#	include <wglew.h>
#endif

#include "pyxieEffekseer.h"
#include <string>

TextureLoaderFunc pyxieEffekseer::textureLoaderFunc = nullptr;

class pyxieTextureLoader : public TextureLoader
{
public:
	pyxieTextureLoader();
	virtual ~pyxieTextureLoader();

public:
	TextureData* Load(const EFK_CHAR* path, TextureType textureType) override;
	void Unload(TextureData* data) override;
};


pyxieTextureLoader::pyxieTextureLoader()
{
}

pyxieTextureLoader::~pyxieTextureLoader()
{
}

static std::u16string getFilenameWithoutExt(const char16_t* path)
{
	int start = 0;
	int end = 0;

	for (int i = start; path[i] != 0; i++)
	{
		if (path[i] == u'.')
		{
			end = i;
		}
	}

	std::vector<char16_t> ret;

	for (int i = start; i < end; i++)
	{
		ret.push_back(path[i]);
	}
	ret.push_back(0);

	return std::u16string(ret.data());
}

TextureData* pyxieTextureLoader::Load(const EFK_CHAR* path, TextureType textureType)
{
	auto _path = getFilenameWithoutExt(path);	

	char path_[300];
	ConvertUtf16ToUtf8((int8_t*)path_, 300, (const int16_t*)_path.c_str());
	if (pyxieEffekseer::textureLoaderFunc != nullptr)
	{
		TextureLoaderCallback callback = { path_ , TextureLoaderType::LOAD};
		auto textureData = pyxieEffekseer::textureLoaderFunc(callback);

		return textureData;
	}
	return new TextureData();
}

void pyxieTextureLoader::Unload(TextureData* data)
{

}

pyxieEffekseer::pyxieEffekseer()
	: manager(nullptr)
	, renderer(nullptr)
	, desiredFramerate(60.0)
	, nextHandle(0)
{
}

pyxieEffekseer::~pyxieEffekseer()
{
	effect_map.clear();
}

void pyxieEffekseer::init()
{	
#if defined(_WIN32)
	renderer = EffekseerRendererGL::Renderer::Create(8000, EffekseerRendererGL::OpenGLDeviceType::OpenGL3);
#else
	renderer = EffekseerRendererGL::Renderer::Create(8000, EffekseerRendererGL::OpenGLDeviceType::OpenGLES3);
#endif
	renderer->SetTextureUVStyle(UVStyle::VerticalFlipped);	// adapt with igeCore.texture

	manager = Manager::Create(8000);

	manager->SetSpriteRenderer(renderer->CreateSpriteRenderer());
	manager->SetRibbonRenderer(renderer->CreateRibbonRenderer());
	manager->SetRingRenderer(renderer->CreateRingRenderer());
	manager->SetTrackRenderer(renderer->CreateTrackRenderer());
	manager->SetModelRenderer(renderer->CreateModelRenderer());

	manager->SetTextureLoader(new pyxieTextureLoader()); //renderer->CreateTextureLoader() || new pyxieTextureLoader()
	manager->SetModelLoader(renderer->CreateModelLoader());
	manager->SetMaterialLoader(renderer->CreateMaterialLoader());
}

void pyxieEffekseer::release()
{
	for (auto it = effect_map.begin(); it != effect_map.end(); it++)
	{
		(*it).second.effect->Release();
	}
	effect_map.clear();

	if (manager != nullptr)
	{
		manager->Destroy();
		manager = nullptr;
	}

	if (renderer != nullptr)
	{
		renderer->Destroy();
		renderer = nullptr;
	}
}

void pyxieEffekseer::update(float dt)
{
	renderer->SetProjectionMatrix(projection_mat);
	renderer->SetCameraMatrix(view_mat);

	auto it = effect_map.begin();
	auto it_end = effect_map.end();

	while(it != it_end)
	{	
		Handle handle = (*it).second.handle;
		if (!manager->Exists(handle))
		{
			if ((*it).second.isLooping)
			{
				if ((*it).second.isShown)
				{
					auto effect = (*it).second.effect;
					Handle hd = manager->Play(effect, (*it).second.position);
					manager->SetScale(hd, (*it).second.scale.X, (*it).second.scale.Y, (*it).second.scale.Z);
					effect_map[(*it).first].handle = hd;
					for (int i = 0; i < 4; i++)
					{
						manager->SetDynamicInput(hd, i, (*it).second.dynamic_inputs[i]);
					}
					effect->AddRef();
				}
				++it;				
			}
			else
			{
				(*it).second.effect->Release();
				effect_map.erase(it++);
			}
		}
		else
		{
			++it;
		}
	}

	manager->Update(desiredFramerate * dt);	
}

uint32_t pyxieEffekseer::play(const char* name, bool loop, const Effekseer::Vector3D& position, const Vector3D& rotation, const Vector3D& scale)
{
	uint32_t handle = nextHandle;	
	nextHandle++;

	EFK_CHAR path[300];
	ConvertUtf8ToUtf16((int16_t*)path, 300, (const int8_t*)name);

	auto _effect = Effect::Create(manager, path);	
	int hd = manager->Play(_effect, position);
	SetLocation(hd, position);
	SetRotation(hd, rotation.X, rotation.Y, rotation.Z);
	SetScale(hd, scale.X, scale.Y, scale.Z);

	effect_map[handle] = { hd, _effect, loop, true, position, rotation, scale };

	_effect->AddRef();
	
	return handle;
}

void pyxieEffekseer::stop(int handle)
{
	Handle hd = 0;
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		hd = (*it).second.handle;
		(*it).second.effect->Release();
		effect_map.erase(it);
	}
	
	if (manager->Exists(hd))
	{
		manager->StopEffect(hd);
	}
}

void pyxieEffekseer::stopAll()
{
	manager->StopAllEffects();

	for (auto it = effect_map.begin(); it != effect_map.end(); it++)
	{
		(*it).second.effect->Release();
	}
	effect_map.clear();
}

void pyxieEffekseer::clearScreen()
{
    glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);
}

void pyxieEffekseer::setup(bool isClear)
{
#if defined(__ANDROID__) || TARGET_OS_IPHONE
    int fbo = 0;
    glGetIntegerv(GL_FRAMEBUFFER_BINDING, &fbo);
    glBindFramebuffer(GL_FRAMEBUFFER, fbo);    
#endif

	if (isClear)
	{
		clearScreen();
	}
}

void pyxieEffekseer::render(bool isClear)
{
	setup(isClear);

	renderer->BeginRendering();
	manager->Draw();
	renderer->EndRendering();
}

int32_t pyxieEffekseer::getDrawcallCount()
{
	int32_t count = renderer->GetDrawCallCount();
	renderer->ResetDrawCallCount();

	return count;
}

int32_t pyxieEffekseer::getDrawVertexCount()
{
	int32_t count = renderer->GetDrawVertexCount();
	renderer->ResetDrawVertexCount();

	return count;
}

int32_t pyxieEffekseer::getUpdateTime()
{
	return manager->GetUpdateTime();
}

int32_t pyxieEffekseer::getDrawTime()
{
	return manager->GetDrawTime();
}

int32_t pyxieEffekseer::getInstanceCount(Handle handle)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		return manager->GetInstanceCount(hd);
	}
	return 0;
}

int32_t pyxieEffekseer::getTotalInstanceCount()
{
	return manager->GetTotalInstanceCount();
}

void pyxieEffekseer::setTextureLoader(TextureLoaderFunc loader)
{
	textureLoaderFunc = loader;
}

void pyxieEffekseer::SetTargetLocation(Handle handle, float x, float y, float z)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		manager->SetTargetLocation(hd, x, y, z);
	}	
}

const Vector3D& pyxieEffekseer::GetLocation(Handle handle)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		return manager->GetLocation(hd);
	}	
}
void pyxieEffekseer::SetLocation(Handle handle, float x, float y, float z)
{
	SetLocation(handle, Vector3D(x, y, z));
}

void pyxieEffekseer::SetLocation(Handle handle, const Vector3D& location)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		it->second.position = location;
		Handle hd = it->second.handle;
		manager->SetLocation(hd, location);
	}
}

void pyxieEffekseer::SetRotation(Handle handle, float x, float y, float z)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		it->second.rotation = Vector3D(x, y, z);
		Handle hd = it->second.handle;
		manager->SetRotation(hd, x, y, z);
	}
}

void pyxieEffekseer::SetScale(Handle handle, float x, float y, float z)
{	
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		it->second.scale = Vector3D(x, y, z);
		Handle hd = it->second.handle;
		manager->SetScale(hd, x, y, z);
	}
}

void pyxieEffekseer::SetAllColor(Handle handle, Color color)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		manager->SetAllColor(hd, color);
	}	
}

void pyxieEffekseer::SetSpeed(Handle handle, float speed)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		manager->SetSpeed(hd, speed);
	}	
}

float pyxieEffekseer::GetSpeed(Handle handle)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		return manager->GetSpeed(hd);
	}
	return 0.0;	
}

bool pyxieEffekseer::IsPlaying(Handle handle)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		return manager->Exists(hd);
	}
	return false;
}

void pyxieEffekseer::SetPause(Handle handle, bool paused)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		manager->SetPaused(hd, paused);
	}
}

bool pyxieEffekseer::GetPause(Handle handle)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		return manager->GetPaused(hd);
	}
	return false;	
}

void pyxieEffekseer::SetShown(Handle handle, bool shown, bool reset)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		it->second.isShown = shown;
		Handle hd = it->second.handle;
		manager->SetShown(hd, shown);
		if (reset)
		{
			manager->UpdateHandleToMoveToFrame(hd, 0);
		}
	}	
}

bool pyxieEffekseer::GetShown(Handle handle)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		Handle hd = it->second.handle;
		return manager->GetShown(hd);
	}
	return false;
}

void pyxieEffekseer::SetLoop(Handle handle, bool loop)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		it->second.isLooping = loop;
	}
}

bool pyxieEffekseer::GetLoop(Handle handle)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		return it->second.isLooping;
	}
	return false;
}

void pyxieEffekseer::SetRenderProjectionMatrix(float* projection)
{
	memcpy(projection_mat.Values, projection, sizeof(float) * 16);
}

void pyxieEffekseer::SetRenderViewMatrix(float* view_inv)
{
	memcpy(view_mat.Values, view_inv, sizeof(float) * 16);
}

void pyxieEffekseer::setDynamicInput(uint32_t handle, float* value)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		memcpy(it->second.dynamic_inputs, value, sizeof(float) * 4);
		Handle hd = it->second.handle;
		for (int i = 0; i < 4; i++)
		{
			manager->SetDynamicInput(hd, i, value[i]);
		}
	}
}

float* pyxieEffekseer::getDynamicInput(uint32_t handle)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		return it->second.dynamic_inputs;
	}
	float buff[4] = { 0.0, 0.0, 0.0, 0.0 };
	return buff;
}