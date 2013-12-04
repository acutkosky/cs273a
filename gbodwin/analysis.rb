class Hash
    def normalize
        count = values.inject(0, :+)
        keys.each{|key| self[key] /= count.to_f}
    end
    
    def correlationWith otherHash
        count = 0
        keys.each do |key|
            count += [self[key], otherHash[key]].min
        end
        count
    end
end

corrMatr = Hash.new(nil)
puts ARGV[0]
h1fname = Dir.entries("ser1").select{|e| e.include? "SER"}[ARGV[0].to_i]


    
        h1fname.slice! "SER"
        puts "Handling #{h1fname}"
        corrMatr[h1fname] = Hash.new(nil)
        h1Hash = Marshal::load(File.new("ser1/SER" + h1fname, "r").read)[h1fname]
        h1Hash.normalize
        
        Dir.entries("IMR90CellLine/ser1").each do |imrfname|
            if imrfname.include? "SER"
                imrfname.slice! "SER"
                puts "\tHandling #{imrfname}"
                imrHash = Marshal::load(File.new("IMR90CellLine/ser1/SER" + imrfname).read)
                imrHash.normalize
                
                corrMatr[h1fname][imrfname] = h1Hash.correlationWith imrHash
                puts corrMatr[h1fname][imrfname]
            end
        end
    


  File.new("CorrMatr#{ARGV[0]}", "w").write(Marshal::dump(corrMatr))

=begin
cm = Marshal::load(File.new("CorrMatr", "r").read)

# squareify the hash
cm.keys.each do |key1|
    cm.keys.each do |key2|
        if cm[key1][key2]
            cm[key2][key1] = cm[key1][key2]
        else
            cm[key1][key2] = cm[key2][key1]
        end
    end
end

outfile = File.new("CorrMatrTSV", "w")
outfile.puts cm.keys.join("\t")
print "\{"
cm.keys.each do |key1|
    print "\{"
    cm.keys.each do |key2|
        print cm[key1][key2]
        print ", "
    end
    print "\}, "
    puts
end
print "\}"
=end
