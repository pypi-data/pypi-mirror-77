#include "igeSound.h"
#include "igeSound_doc_en.h"

static void pyObjToFloat(PyObject* obj, float* f, int& d) {
	if (f) {
		f[0] = f[1] = f[2] = 0.0f;
	}

	if (obj)
	{
		if (PyTuple_Check(obj)) {
			d = (int)PyTuple_Size(obj);
			if (d > 3) d = 3;
			for (int j = 0; j < d; j++) {
				PyObject* val = PyTuple_GET_ITEM(obj, j);
				f[j] = (float)PyFloat_AsDouble(val);
			}
		}
		else if (PyList_Check(obj)) {
			d = (int)PyList_Size(obj);
			if (d > 3) d = 3;
			for (int j = 0; j < d; j++) {
				PyObject* val = PyList_GET_ITEM(obj, j);
				f[j] = (float)PyFloat_AsDouble(val);
			}
		}
	}
}

PyObject* igeSound_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	igeSound_obj* self = NULL;

	self = (igeSound_obj*)type->tp_alloc(type, 0);
	self->sound = Sound::Instance();

	return (PyObject*)self;
}

void igeSound_dealloc(igeSound_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* igeSound_str(igeSound_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "igeSound object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* igeSound_Init(igeSound_obj* self)
{
	Sound::Instance()->init();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_Release(igeSound_obj* self)
{
	Sound::Instance()->release();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_Update(igeSound_obj* self)
{
	Sound::Instance()->update();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_Play(igeSound_obj* self, PyObject* args, PyObject* kwargs)
{
	PyObject* sound_obj;
	int stream = 0;
	int loop = 0;
	int is_3d = 0;
	float volume = -1.0f;
	PyObject* position = nullptr;

	static char* kwlist[] = { "name", "stream", "loop", "is_3d", "position", "volume", NULL };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|iiiOf", kwlist, &sound_obj, &stream, &loop, &is_3d, &position, &volume)) return NULL;

	int d1;
	float buff[3] = { 0.0, 0.0, 0.0 };
	pyObjToFloat((PyObject*)position, buff, d1);

	int handle = -1;
	if (PyLong_Check(sound_obj))
	{
		int preset_id = PyLong_AsLong(sound_obj);
		handle = Sound::Instance()->playPreset(preset_id, loop, is_3d, buff[0], buff[1], buff[2], volume);
	}
	else
	{
		const char* soundName = PyUnicode_AsUTF8(sound_obj);
		handle = Sound::Instance()->play(soundName, stream, loop, is_3d, buff[0], buff[1], buff[2], volume);
	}

	
	return PyLong_FromLong(handle);
}

static PyObject* igeSound_Stop(igeSound_obj* self, PyObject* args)
{
	PyObject* sound_obj;
	if (!PyArg_ParseTuple(args, "O", &sound_obj))
		return NULL;

	if (PyLong_Check(sound_obj))
	{
		int handle = PyLong_AsLong(sound_obj);
		Sound::Instance()->stop(handle);
	}
	else
	{
		const char* soundName = PyUnicode_AsUTF8(sound_obj);
		Sound::Instance()->stop(soundName);
	}

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_StopAll(igeSound_obj* self)
{
	Sound::Instance()->stopAllSound();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_Load(igeSound_obj* self, PyObject* args)
{
	char* soundName;
	int stream = 0;
	if (!PyArg_ParseTuple(args, "s|i", &soundName, &stream))
		return NULL;

	Sound::Instance()->load(soundName, stream);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_Unload(igeSound_obj* self, PyObject* args)
{
	char* soundName;
	if (!PyArg_ParseTuple(args, "s", &soundName))
		return NULL;

	Sound::Instance()->unload(soundName);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_FadeVolume(igeSound_obj* self, PyObject* args)
{
	int handle = 0;
	float aTo = 0.0f;
	float aTime = 0.0f;
	if (!PyArg_ParseTuple(args, "iff", &handle, &aTo, &aTime))
		return NULL;

	Sound::Instance()->fadeVolume(handle, aTo, aTime);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_ScheduleStop(igeSound_obj* self, PyObject* args)
{
	int handle = 0;
	float aTime = 0.0f;
	if (!PyArg_ParseTuple(args, "if", &handle, &aTime))
		return NULL;

	Sound::Instance()->scheduleStop(handle, aTime);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_setGlobalVolume(igeSound_obj* self, PyObject* args)
{
	float volume = 1.0;
	if (!PyArg_ParseTuple(args, "f", &volume))
		return NULL;

	Sound::Instance()->setGlobalVolume(volume);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_getGlobalVolume(igeSound_obj* self)
{
	return PyFloat_FromDouble(Sound::Instance()->getGlobalVolume());
}

static PyObject* igeSound_getStreamTime(igeSound_obj* self, PyObject* args)
{
	int handle = 0;
	if (!PyArg_ParseTuple(args, "i", &handle))
		return NULL;
	return PyFloat_FromDouble(Sound::Instance()->getStreamTime(handle));
}

static PyObject* igeSound_set3dSourcePosition(igeSound_obj* self, PyObject* args)
{
	int handle = 0;
	PyObject* position;
	if (!PyArg_ParseTuple(args, "iO", &handle, &position))
		return NULL;

	int d1;
	float buff[3] = { 0.0, 0.0, 0.0 };
	pyObjToFloat((PyObject*)position, buff, d1);
	Sound::Instance()->set3dSourcePosition(handle, buff[0], buff[1], buff[2]);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_set3dMinMaxDistance(igeSound_obj* self, PyObject* args)
{
	int handle = 0;
	PyObject* position;
	if (!PyArg_ParseTuple(args, "iO", &handle, &position))
		return NULL;

	int d1;
	float buff[3] = { 0.0, 0.0, 0.0 };
	pyObjToFloat((PyObject*)position, buff, d1);
	Sound::Instance()->set3dMinMaxDistance(handle, buff[0], buff[1]);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* igeSound_set3dAttenuation(igeSound_obj* self, PyObject* args)
{
	int handle = 0;
	int mode = 0;
	float rolloffFactor = 0.25;
	if (!PyArg_ParseTuple(args, "iif", &handle, &mode , &rolloffFactor))
		return NULL;

	Sound::Instance()->set3dAttenuation(handle, mode, rolloffFactor);

	Py_INCREF(Py_None);
	return Py_None;
}

PyMethodDef igeSound_methods[] = {
	{ "init", (PyCFunction)igeSound_Init, METH_NOARGS, soundInit_doc },
	{ "release", (PyCFunction)igeSound_Release, METH_NOARGS, soundRelease_doc },
	{ "update", (PyCFunction)igeSound_Update, METH_NOARGS, soundUpdate_doc },
	{ "play", (PyCFunction)igeSound_Play, METH_VARARGS | METH_KEYWORDS, soundPlay_doc },
	{ "stop", (PyCFunction)igeSound_Stop, METH_VARARGS, soundStop_doc },
	{ "stopAll", (PyCFunction)igeSound_StopAll, METH_NOARGS, soundStopAll_doc },
	{ "load", (PyCFunction)igeSound_Load, METH_VARARGS, soundLoad_doc },
	{ "unload", (PyCFunction)igeSound_Unload, METH_VARARGS, soundUnload_doc },
	{ "fadeVolume", (PyCFunction)igeSound_FadeVolume, METH_VARARGS, soundFadeVolume_doc },
	{ "scheduleStop", (PyCFunction)igeSound_ScheduleStop, METH_VARARGS, soundScheduleStop_doc },
	{ "setGlobalVolume", (PyCFunction)igeSound_setGlobalVolume, METH_VARARGS, soundSetGlobalVolume_doc },
	{ "getGlobalVolume", (PyCFunction)igeSound_getGlobalVolume, METH_NOARGS, soundGetGlobalVolume_doc },
	{ "getStreamTime", (PyCFunction)igeSound_getStreamTime, METH_VARARGS, soundGetStreamTime_doc },
	{ "set3dSourcePosition", (PyCFunction)igeSound_set3dSourcePosition, METH_VARARGS, soundSet3dSourcePosition_doc },
	{ "set3dMinMaxDistance", (PyCFunction)igeSound_set3dMinMaxDistance, METH_VARARGS, soundSet3dMinMaxDistance_doc },
	{ "set3dAttenuation", (PyCFunction)igeSound_set3dAttenuation, METH_VARARGS, soundSet3dAttenuation_doc },
	{ NULL,	NULL }
};

PyGetSetDef igeSound_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject IgeSoundType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeSound.sound",					/* tp_name */
	sizeof(igeSound_obj),				/* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)igeSound_dealloc,		/* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,					                /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)igeSound_str,				/* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	0,									/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	igeSound_methods,					/* tp_methods */
	0,                                  /* tp_members */
	igeSound_getsets,					/* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	igeSound_new,						/* tp_new */
	0,									/* tp_free */
};

static PyModuleDef igeSound_module = {
	PyModuleDef_HEAD_INIT,
	"igeSound",							// Module name to use with Python import statements
	"IGE Sound Module.",				// Module description
	0,
	igeSound_methods					// Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_igeSound() {
	PyObject* module = PyModule_Create(&igeSound_module);

	if (PyType_Ready(&IgeSoundType) < 0) return NULL;

	PyModule_AddIntConstant(module, "SFXR_COIN", 0);
	PyModule_AddIntConstant(module, "SFXR_LASER", 1);
	PyModule_AddIntConstant(module, "SFXR_EXPLOSION", 2);
	PyModule_AddIntConstant(module, "SFXR_POWERUP", 3);
	PyModule_AddIntConstant(module, "SFXR_HURT", 4);
	PyModule_AddIntConstant(module, "SFXR_JUMP", 5);
	PyModule_AddIntConstant(module, "SFXR_BLIP", 6);

	PyModule_AddIntConstant(module, "NO_ATTENUATION", 0);
	PyModule_AddIntConstant(module, "INVERSE_DISTANCE", 1);
	PyModule_AddIntConstant(module, "LINEAR_DISTANCE", 2);
	PyModule_AddIntConstant(module, "EXPONENTIAL_DISTANCE", 3);	

	return module;
}