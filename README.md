# Procjena gustoće mnoštva ljudi utemeljena lokalnim binarnim značajkama

Na temelju rada Z. Wang et al. "Crowd Density Estimation Based On Local Binary Pattern Co-Occurrence
Matrix" oblikovati sustav za procjenu gustoće mnoštva ljudi koji se temelji na lokalnim binarnim značajkama,
matrici pojavnosti i Haralickovim teksturnim značajkama. Oblikovani sustav neka se sastoji od dva
podsustava od kojih se jedan temelji na lokalnim binarnim značajkama dobivenih iz sivih slika a drugi na
lokalnm binarnim značajkama generiranih na gradijentnim slikama. Ocijeniti točnost klasifikacije za svaki od
podsustava i to za postupak klasifikacije na temelju k-NN klasifikatora i stroja s potpornim vektorima (SVM).
Nakon ispitivanja oba podsustava oblikovati sustav koji se temelji na fuziji obaju podsustava na razini
donošenja konačne odluke. Iscrpno opisati fazu učenja i fazu klasifikacije te ocijeniti utjecaj dimenzije vektora
značajki koji se sastoji od n > 4 Haralikovih teksturnih značajki. Prikazati rezultate klasifikacije za različite
veličine i korake pomaka kliznog okna. Ispitivanje uspješnosti oblikovanih podsustava i sustava izvesti na
skupu slika PETS 2009 te ih usporediti s rezultatima dobivenim u gore navedenom radu. Uz to, izabrati skup
slika s velikim mnoštvom ljudi (izvor: Internet; High Density Crowd) te ocijeniti prikladnost postupka za
procjenu broja ljudi, odnosno gustoće ljudi na jedinicu površine (umjesto klasifikacije u pet razreda). Radu
priložiti baze slika za učenje i testiranje, programe s uputama za korištenje, opis GUI-a, rezultate klasifikacije
i popis korištene literature.
