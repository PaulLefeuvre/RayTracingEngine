from hittable import *

class hittable_list:
    def __init__(self):
        self.objects = []
    def clear(self):
        self.objects = []
    def add(self, obj):
        self.objects.append(obj)

    def hit(self, r, t_min, t_max, rec):
        hit_anything = False
        closest_so_far = t_max

        for obj in self.objects:
            temp_rec = hit_record()
            temp_rec = obj.hit(r, t_min, closest_so_far, temp_rec)
            if(temp_rec != None):
                hit_anything = True
                closest_so_far = temp_rec.t
                rec = temp_rec

        if(hit_anything):
            return rec
        else:
            return None
