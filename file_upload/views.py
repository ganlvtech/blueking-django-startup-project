from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render


def index(request):
    if request.method == 'POST' and request.FILES['file']:
        """Simple File Upload
        https://github.com/sibtc/simple-file-upload
        """
        from django.core.files.storage import FileSystemStorage

        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'file_upload/index.html', {
            'ok': True,
            'uploaded_file_url': uploaded_file_url,
        })

    import os
    from myutils.utils import format_time
    from mysite import settings
    document_root = settings.MEDIA_ROOT.decode('utf-8')

    _files = []

    if os.path.exists(document_root):
        file_names = os.listdir(document_root)
        for filename in file_names:
            full_path = os.path.join(document_root, filename)
            file_stat = os.stat(full_path)
            _files.append({
                'name': filename,
                'mode': oct(file_stat.st_mode & 0o777),
                'size': file_stat.st_size,
                'date': format_time(file_stat.st_mtime)
            })

    return render(request, 'file_upload/index.html', {
        'files': _files
    })


def delete(request):
    if request.method != 'DELETE' and (request.method != 'POST' or request.POST.get('_method') != 'DELETE'):
        return HttpResponseRedirect(reverse('upload:index'))

    import os
    from mysite import settings
    from .utils import sanitize_path

    path = request.POST.get('path')
    if not path:
        raise ValidationError('path must be set')

    newpath = sanitize_path(path)
    if newpath and path != newpath:
        return HttpResponseBadRequest('path should be {} instead of {}'.format(newpath, path))

    document_root = settings.MEDIA_ROOT
    fullpath = os.path.join(document_root, newpath)

    if not os.path.exists(fullpath):
        return HttpResponseRedirect(reverse('upload:index'))

    os.unlink(fullpath)
    return render(request, 'file_upload/delete.html', {
        'file_deleted': path,
    })
