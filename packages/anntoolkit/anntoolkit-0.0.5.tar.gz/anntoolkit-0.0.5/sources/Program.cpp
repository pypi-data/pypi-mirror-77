#include "Shader.h"
#include <stdio.h>
#include <spdlog/spdlog.h>
#include <GL/gl3w.h>
#include <glm/glm.hpp>
#include <glm/gtx/quaternion.hpp>
#include <type_traits>
#include <map>


namespace Render
{
	Program::Program()
	{
		m_program = glCreateProgram();
	}

	Program::~Program()
	{
		glDeleteProgram(m_program);
	}

	bool Program::LinkImpl()
	{
		glLinkProgram(m_program);

		int linked;
		glGetProgramiv(m_program, GL_LINK_STATUS, &linked);
		if (!linked)
		{
			GLint infoLen = 0;
			glGetProgramiv(m_program, GL_INFO_LOG_LENGTH, &infoLen);
			if (infoLen > 1)
			{
				char* buf = new char[infoLen];
				glGetProgramInfoLog(m_program, infoLen, nullptr, buf);
				spdlog::warn("Linking error: \n{}\n", buf);
				delete[] buf;
				return false;
			}
		}
		InitUniforms();
		return true;
	}

	void Program::InitUniforms()
	{
		int total = -1;
		glGetProgramiv(m_program, GL_ACTIVE_UNIFORMS, &total);

		m_uniforms.clear();

		for (int i = 0; i < total; ++i)
		{
			int name_len = -1, num = -1;
			GLenum type = GL_ZERO;
			char name[256];
			glGetActiveUniform(m_program, GLuint(i), sizeof(name) - 1, &name_len, &num, &type, name);
			name[name_len] = 0;
			GLuint location = glGetUniformLocation(m_program, name);
			Uniform u(location, VarType::FromGLMapping(type), num);
			m_uniforms.push_back(u);
			m_uniformMap[name] = static_cast<int>(m_uniforms.size()) - 1;
		}
	}

	class Attacher
	{
		Attacher(const Attacher& other) = delete;
		Attacher& operator=(const Attacher&) = delete;
	public:
		Attacher(GLuint program, GLuint shader) :program(program), shader(shader)
		{
			glAttachShader(program, shader);
		}
		~Attacher()
		{
			glDetachShader(program, shader);
		}
	private:
		GLuint program;
		GLuint shader;
	};

	bool Program::Link(const Shader<SHADER_TYPE::COMPUTE_SHADER>& shader)
	{
		Attacher attacher(m_program, shader.m_shader);
		return LinkImpl();
	}

	bool Program::Link(const Shader<SHADER_TYPE::VERTEX_SHADER>& vs, const Shader<SHADER_TYPE::FRAGMENT_SHADER>& fs)
	{
		Attacher attacher_vs(m_program, vs.m_shader);
		Attacher attacher_fs(m_program, fs.m_shader);
		return LinkImpl();
	}

	bool Program::Link(const Shader<SHADER_TYPE::VERTEX_SHADER>& vs, const Shader<SHADER_TYPE::GEOMETRY_SHADER>& gs, const Shader<SHADER_TYPE::FRAGMENT_SHADER>& fs)
	{
		Attacher attacher_vs(m_program, vs.m_shader);
		Attacher attacher_gs(m_program, gs.m_shader);
		Attacher attacher_fs(m_program, fs.m_shader);
		return LinkImpl();
	}

	void Program::Use() const
	{
		glUseProgram(m_program);
	}

	int Program::GetAttribLocation(const char *name) const
	{
		return glGetAttribLocation(m_program, name);
	}

	int Program::GetUniformLocation(const char *name) const
	{
		return glGetUniformLocation(m_program, name);
	}

	Uniform Program::GetUniform(const char* name)
	{
		std::string n(name);
		auto it = m_uniformMap.find(name);
		if (it != m_uniformMap.end())
		{
			return m_uniforms[it->second];
		}
		return Uniform(-1, VarType::INVALID, 0);
	}

	ProgramPtr MakeProgram(const char* vertex_shader, const char* fragment_shader)
	{
		bool succeeded = true;
		Shader<SHADER_TYPE::VERTEX_SHADER> vs;
		succeeded &= vs.CompileShader(vertex_shader);
		Shader<SHADER_TYPE::FRAGMENT_SHADER> fs;
		succeeded &= fs.CompileShader(fragment_shader);
		ProgramPtr program(new Program);
		succeeded &= program->Link(vs, fs);
		if (succeeded)
		{
			return program;
		}
		return nullptr;
	}

	template<typename T>
	void Uniform::ApplyValue(const T& value) const
	{
		spdlog::error("Unsupported type");
		assert(false);
	}

	template<typename T>
	void Uniform::ApplyValue(const T* value, int count) const
	{
		spdlog::error("Unsupported type");
		assert(false);
	}

	template<>
	void Uniform::ApplyValue<int>(const int& value) const
	{
		assert(VarType::IsSignedInteger(m_type) || VarType::IsSampler(m_type) );
		glUniform1iv(m_handle, 1, reinterpret_cast<const GLint*>(&value));
	}

	template<>
	void Uniform::ApplyValue<int>(const int* value, int count) const
	{
		assert(VarType::IsSignedInteger(m_type) || VarType::IsSampler(m_type) );
		glUniform1iv(m_handle, count, reinterpret_cast<const GLint*>(value));
	}

	template<>
	void Uniform::ApplyValue<unsigned int>(const unsigned int& value) const
	{
		assert(VarType::IsUnsignedInteger(m_type) || VarType::IsSampler(m_type) );
		glUniform1uiv(m_handle, 1, reinterpret_cast<const unsigned int*>(&value));
	}

	template<>
	void Uniform::ApplyValue<unsigned int>(const unsigned int* value, int count) const
	{
		assert(VarType::IsUnsignedInteger(m_type) || VarType::IsSampler(m_type) );
		glUniform1uiv(m_handle, count, reinterpret_cast<const unsigned int*>(value));
	}

#define ADD_SPEC(C, T, T2, TA) \
	template<> \
	void Uniform::ApplyValue<TA>(const TA& value) const \
	{ \
		assert(m_type == VarType::GetType<TA>()); \
		glUniform##C##T##v(m_handle, 1, reinterpret_cast<const T2*>(&value)); \
	} \
	template<> \
	void Uniform::ApplyValue<TA>(const TA* value, int count) const \
	{ \
		assert(m_type == VarType::GetType<TA>()); \
		glUniform##C##T##v(m_handle, count, reinterpret_cast<const T2*>(value)); \
	}

#define ADD_SPEC_M(C, T, T2, TA) \
	template<> \
	void Uniform::ApplyValue<TA>(const TA& value) const \
	{ \
		assert(m_type == VarType::GetType<TA>()); \
		glUniformMatrix##C##T##v(m_handle, 1, false, reinterpret_cast<const T2*>(&value)); \
	} \
	template<> \
	void Uniform::ApplyValue<TA>(const TA* value, int count) const \
	{ \
		assert(m_type == VarType::GetType<TA>()); \
		glUniformMatrix##C##T##v(m_handle, 1, false, reinterpret_cast<const T2*>(value)); \
	}

#define ADD_SPEC_A(C, T, T2, TA) \
	template<> \
	void Uniform::ApplyValue<TA>(const std::vector<TA>& value) const \
	{ \
		assert(m_type == VarType::GetType<TA>()); \
		glUniform##C##T##v(m_handle, static_cast<GLsizei>(value.size()), reinterpret_cast<const T2*>(value.data())); \
	}

	ADD_SPEC(1, f, float, float)
	ADD_SPEC(2, f, float, glm::vec2)
	ADD_SPEC(3, f, float, glm::vec3)
	ADD_SPEC(4, f, float, glm::vec4)
	ADD_SPEC(4, f, float, glm::quat)

	ADD_SPEC(2, i, int, glm::ivec2)
	ADD_SPEC(3, i, int, glm::ivec3)
	ADD_SPEC(4, i, int, glm::ivec4)

	ADD_SPEC_M(2, f, float, glm::mat2)
	ADD_SPEC_M(3, f, float, glm::mat3)
	ADD_SPEC_M(4, f, float, glm::mat4)

	ADD_SPEC_A(1, f, float, float)
	ADD_SPEC_A(2, f, float, glm::vec2)
	ADD_SPEC_A(3, f, float, glm::vec3)
	ADD_SPEC_A(4, f, float, glm::vec4)
	ADD_SPEC_A(4, f, float, glm::quat)

	ADD_SPEC_A(2, i, int, glm::ivec2)
	ADD_SPEC_A(3, i, int, glm::ivec3)
	ADD_SPEC_A(4, i, int, glm::ivec4)
}

#include <doctest.h>

TEST_CASE("[Render] Shaders")
{
	SUBCASE("Basic")
	{
		const char* vertex_shader_src = R"(
			attribute vec3 a_position;
			attribute vec2 a_uv;
			uniform mat4 u_modelView;
			uniform mat4 u_projection;
			varying vec2 v_uv;

			void main()
			{
				vec4 pos = u_modelView * vec4(a_position, 1.0);
				gl_Position = u_projection * pos;
			}
		)";

		const char* fragment_shader_src = R"(
			varying vec2 v_uv;
			uniform sampler2D u_texture;

			void main()
			{
				vec3 color = texture2D(u_texture, v_uv).rgb;
				color = pow(color, vec3(2.2));
				gl_FragColor = vec4(pow(color, vec3(1.0/2.2)), 1.0);
			}
		)";

		auto program = Render::MakeProgram(vertex_shader_src, fragment_shader_src);
		CHECK(program);

		auto modelView = program->GetUniformLocation("u_modelView");
		auto projection = program->GetUniformLocation("u_projection");
		auto uniform_texture = program->GetUniformLocation("u_texture");

		auto does_not_exist = program->GetUniformLocation("does_not_exist");

		CHECK_NE(modelView, -1);
		CHECK_NE(projection, -1);
		CHECK_NE(uniform_texture, -1);
		CHECK_EQ(does_not_exist, -1);

		program->GetUniform("u_texture").ApplyValue(1);
		program->GetUniform("u_projection").ApplyValue(glm::mat4(1.0));

//		REQUIRE_THROWS({
//			Render::Uniform aa(-1, Render::VarType::BYTE, 1);
//			aa.ApplyValue("!");
//		});


	}
}
