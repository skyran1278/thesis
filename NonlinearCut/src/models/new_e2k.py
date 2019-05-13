"""
write to new e2k
"""
import shlex
import warnings

from src.models.e2k import E2k
from src.models.defaultdict_enhance import DefaultdictEnhance


class NewE2k(E2k):
    """
    use to write new e2k
    """

    def __init__(self, *args, **kwargs):
        self.f = None
        self.line_hinges = DefaultdictEnhance()
        # self.new_lines = Lines()
        super(NewE2k, self).__init__(*args, **kwargs)

    def post_point_coordinates(self, coordinates):
        """
        post list of coordinates to point_coordinates
        """
        point_keys = []
        for coor in coordinates:
            point_keys.append(self.point_coordinates.post(value=coor))

        return point_keys

    def post_lines(self, point_keys):
        """
        post list of coordinates to lines
        """
        line_keys = []
        # coor_id = []
        # for coor in coordinates:
        #     coor_id.append(self.point_coordinates.get(value=coor))

        length = len(point_keys) - 1
        index = 0
        while index < length:
            line_keys.append(self.lines.post(
                value=[point_keys[index], point_keys[index + 1]]
            ))
            index += 1

        return line_keys

    def post_sections(self, rebars, copy_from):
        """
        post list of coordinates to lines
        """
        new_sections = []

        length = len(rebars) - 1
        index = 0
        while index < length:
            ati = rebars[index][0]
            abi = rebars[index][1]
            atj = rebars[index + 1][0]
            abj = rebars[index + 1][1]

            new_section = f'{copy_from} {ati} {abi} {atj} {abj}'

            data = {
                'ATI': ati,
                'ABI': abi,
                'ATJ': atj,
                'ABJ': abj
            }

            self.sections.post(new_section, data, copy_from)

            index += 1

            new_sections.append(new_section)

        return new_sections

    def post_point_assigns(self, points, story):
        """
        combine line and section

        """
        start = self.point_assigns.get(key=(story, points[0]))
        end = self.point_assigns.get(key=(story, points[-1]))

        if start != end:
            warnings.warn(f'Warning start key {start} != end key {end}')

        # points maybe have no assigns
        # if start is {}, then return
        if start is None:
            return

        for point in points[1: -1]:
            self.point_assigns.post(
                key=(story, point), copy_from=(story, points[0])
            )

    def post_line_assigns(self, lines, sections, copy_from):
        """
        combine line and section
        v9 to v16 may change line name
            if error occur, check it and modify excel to match new line name
        """
        story, _ = copy_from
        for line, section in zip(lines, sections):
            self.line_assigns.post(
                key=(story, line),
                value={
                    'SECTION': section
                },
                copy_from=copy_from
            )

        # lines more than one
        # then can delete origin line
        if not len(lines) == 1:
            self.line_assigns.delete(copy_from)

    def post_line_hinges(self, lines, story):
        """
        post hinge
        """
        for line in lines:
            self.line_hinges.post((story, line), ('M3', 0))

        self.line_hinges.post((story, lines[-1]), ('M3', 1))

    def post_line_loads(self, lines, copy_from):
        """
        post and delete line loads
        """
        if self.line_loads.get(copy_from) is None:
            return

        story, _ = copy_from

        for line in lines:
            self.line_loads.post((story, line), copy_from=copy_from)

        # lines more than one
        # then can delete origin line
        if not len(lines) == 1:
            self.line_loads.delete(copy_from)

    def _frame_sections(self):
        # pylint: disable=invalid-name
        sections = self.sections.get()
        for section in sections:
            fc = sections[section]['FC']
            D = sections[section]['D']
            B = sections[section]['B']
            propertys = sections[section]['PROPERTIES']
            self.f.write(
                f'FRAMESECTION  "{section}"  MATERIAL "{fc}"  '
                f'SHAPE "Concrete Rectangular"  D {D} B {B} {propertys} \n'
            )

        for section in sections:
            propertys = sections[section]['MODIFICATION PROPERTIES']
            self.f.write(
                f'FRAMESECTION  "{section}"  {propertys}\n')

    def _concrete_sections(self):
        # pylint: disable=invalid-name
        sections = self.sections.get()
        for section in sections:
            fy = sections[section]['FY']
            fyh = sections[section]['FYH']
            cover_top = sections[section]['COVERTOP']
            cover_bot = sections[section]['COVERBOTTOM']
            ati = sections[section]['ATI']
            abi = sections[section]['ABI']
            atj = sections[section]['ATJ']
            abj = sections[section]['ABJ']
            self.f.write(
                f'CONCRETESECTION  "{section}"  LONGBARMATERIAL "{fy}"  '
                f'CONFINEBARMATERIAL "{fyh}"  TYPE "Beam"  COVERTOP {cover_top} '
                f'COVERBOTTOM {cover_bot} ATI {ati} ABI {abi} ATJ {atj} ABJ {abj}\n'
            )

    def _point_coordinates(self):
        coor = self.point_coordinates.get()
        for point in coor:
            start = coor[point][0]
            end = coor[point][1]
            self.f.write(f'POINT "{point}"  {start} {end}\n')

    def _line_connectivities(self):
        columns = self.columns.get()
        beams = self.lines.get()
        for column in columns:
            start, end = columns[column]
            self.f.write(f'LINE  "{column}"  COLUMN  "{start}"  "{end}"  1\n')
        for beam in beams:
            start, end = beams[beam]
            self.f.write(f'LINE  "{beam}"  BEAM  "{start}"  "{end}"  0\n')

    def _point_assigns(self):
        point_assigns = self.point_assigns.get()
        for story, key in point_assigns:
            point_property = point_assigns[(story, key)][0]
            self.f.write(
                f'POINTASSIGN  "{key}"  "{story}"  {point_property}\n'
            )

    def _line_assigns(self):
        line_assigns = self.line_assigns.get()
        for story, key in line_assigns:
            section = line_assigns[(story, key)]['SECTION']
            properties = line_assigns[(story, key)]['PROPERTIES']
            self.f.write(
                f'LINEASSIGN  "{key}"  "{story}"  SECTION "{section}"  {properties}\n'
            )

    def _frame_hinge_assignments(self):
        self.f.write(f'\n$ FRAME HINGE ASSIGNMENTS\n')

        load = self.dead_load_name
        lines_hinges = self.line_hinges.get()

        for line_hinges in lines_hinges:
            story, line = line_hinges
            hinges = lines_hinges[line_hinges]

            for dof, rdistance in hinges:
                self.f.write(
                    f'HINGEASSIGN "{line}"  "{story}"  AUTOHINGETYPE "ASCE41-13"  '
                    f'TABLEITEM "Concrete Beams"  DOF "{dof}"  '
                    f'CASECOMBO "{load}"  RDISTANCE {rdistance}\n'
                )

    def _frame_hinge_overwrites(self):
        self.f.write(f'\n$ FRAME HINGE OVERWRITES\n')

        lines_hinges = self.line_hinges.get()

        for line_hinges in lines_hinges:
            story, line = line_hinges
            self.f.write(
                f'HINGEOVERWRITE "{line}"  "{story}"  AUTOSUBDIVIDERELLENGTH 0.02\n'
            )

    def _frame_object_loads(self):
        lines_loads = self.line_loads.get()
        for line_load in lines_loads:
            loads = lines_loads[line_load]
            story, line = line_load
            for load in loads:
                self.f.write(
                    f'LINELOAD  "{line}"  "{story}"  {load}\n'
                )

    def to_e2k(self, name='new'):
        """
        only call once, write to e2k
        """
        sections = self.sections.get()

        with open(f'{self.path} {name}.e2k', mode='w', encoding='big5') as self.f:
            for line in self.content:
                # skip space line
                if line == '':
                    self.f.write('\n')
                    continue

                if line[0] == '$':
                    # write permission
                    write = True
                    title = line

                if title == '$ FRAME SECTIONS':
                    words = shlex.split(line)
                    section = words[1]
                    if section in sections:
                        continue

                elif title == '$ CONCRETE SECTIONS':
                    words = shlex.split(line)
                    if len(words) > 7 and words[7] == 'Beam':
                        continue

                if write:
                    self.f.write(line)
                    self.f.write('\n')

                if line == '$ FRAME SECTIONS':
                    self._frame_sections()

                elif line == '$ CONCRETE SECTIONS':
                    self._concrete_sections()

                elif line == '$ POINT COORDINATES':
                    write = False
                    self._point_coordinates()

                elif line == '$ LINE CONNECTIVITIES':
                    write = False
                    self._line_connectivities()

                elif line == '$ POINT ASSIGNS':
                    write = False
                    self._point_assigns()

                elif line == '$ LINE ASSIGNS':
                    write = False
                    self._line_assigns()
                    self._frame_hinge_assignments()
                    self._frame_hinge_overwrites()

                elif line == '$ FRAME OBJECT LOADS':
                    write = False
                    self._frame_object_loads()


def main():
    """
    test
    """
    from tests.config import config

    new_e2k = NewE2k(config['e2k_path_test_v1'])

    coordinates = [
        [0., 0.],
        [0.67445007, 0.],
        [0.87367754, 0.],
        [7.12632229, 0.],
        [7.32554951, 0.],
        [8., 0.]
    ]

    point_rebars = [
        (0.0046452, 0.0027097),
        (0.0046452, 0.0027097),
        (0.0046452, 0.0027097),
        (0.0046452, 0.0027097),
        (0.0046452, 0.0027097),
        (0.0046452, 0.0027097)
    ]

    point_keys = new_e2k.post_point_coordinates(coordinates)
    print(point_keys)

    line_keys = new_e2k.post_lines(point_keys)
    print(line_keys)

    section_keys = new_e2k.post_sections('B60X80C28', point_rebars)
    print(section_keys)

    new_e2k.post_point_assigns(point_keys, story='RF')

    new_e2k.post_line_assigns(
        line_keys, section_keys, copy_from=('RF', 'B1'))

    new_e2k.post_line_hinges(line_keys, story='RF')

    new_e2k.post_line_loads(line_keys, ('RF', 'B1'))

    print(new_e2k.point_coordinates.get())
    print(new_e2k.lines.get())
    print(new_e2k.sections.get())
    print(new_e2k.point_assigns.get())
    print(new_e2k.line_assigns.get())
    print(new_e2k.line_hinges.get())
    print(new_e2k.line_loads.get())

    new_e2k.to_e2k()

    print(new_e2k.line_assigns.get())


if __name__ == "__main__":
    main()
