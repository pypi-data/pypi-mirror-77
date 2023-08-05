
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
		Handle handle = (*it).first;
		if (!manager->Exists(handle))
		{
			if ((*it).second.isLooping)
			{
				auto effect = (*it).second.effect;
				Handle hd = manager->Play(effect, (*it).second.position);
				effect_map[hd] = { effect, true, (*it).second.position };
				
				(*it).second.isLooping = false;
				++it;

				effect->AddRef();
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

int pyxieEffekseer::play(const char* name, bool loop, const Effekseer::Vector3D& position)
{
	EFK_CHAR path[300];
	ConvertUtf8ToUtf16((int16_t*)path, 300, (const int8_t*)name);

	auto _effect = Effect::Create(manager, path);	
	int handle = manager->Play(_effect, position);

	effect_map[handle] = { _effect, loop, position};
	_effect->AddRef();
	
	return handle;
}

void pyxieEffekseer::stop(int handle)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		(*it).second.effect->Release();
		effect_map.erase(it);
	}

	if (manager->Exists(handle))
	{
		manager->StopEffect(handle);
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

void pyxieEffekseer::setTextureLoader(TextureLoaderFunc loader)
{
	textureLoaderFunc = loader;
}

void pyxieEffekseer::SetTargetLocation(Handle handle, float x, float y, float z)
{
	manager->SetTargetLocation(handle, x, y, z);
}

const Vector3D& pyxieEffekseer::GetLocation(Handle handle)
{
	return manager->GetLocation(handle);
}
void pyxieEffekseer::SetLocation(Handle handle, float x, float y, float z)
{
	manager->SetLocation(handle, x, y, z);
}

void pyxieEffekseer::SetRotation(Handle handle, float x, float y, float z)
{
	manager->SetRotation(handle, x, y, z);
}

void pyxieEffekseer::SetScale(Handle handle, float x, float y, float z)
{
	manager->SetScale(handle, x, y, z);
}

void pyxieEffekseer::SetAllColor(Handle handle, Color color)
{
	manager->SetAllColor(handle, color);
}

void pyxieEffekseer::SetSpeed(Handle handle, float speed)
{
	manager->SetSpeed(handle, speed);
}

float pyxieEffekseer::GetSpeed(Handle handle)
{
	return manager->GetSpeed(handle);
}

bool pyxieEffekseer::IsPlaying(Handle handle)
{
	return manager->Exists(handle);
}

void pyxieEffekseer::SetPause(Handle handle, bool paused)
{
	manager->SetPaused(handle, paused);
}

bool pyxieEffekseer::GetPause(Handle handle)
{
	return manager->GetPaused(handle);
}

void pyxieEffekseer::SetShown(Handle handle, bool shown)
{
	manager->SetShown(handle, shown);
}

bool pyxieEffekseer::GetShown(Handle handle)
{
	return manager->GetShown(handle);
}

void pyxieEffekseer::SetLoop(Handle handle, bool loop)
{
	auto it = effect_map.find(handle);
	if (it != effect_map.end())
	{
		effect_map[handle].isLooping = loop;
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