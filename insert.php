<?php
header('Content-Type: application/json'); 
// إعدادات الاتصال بقاعدة البيانات
$host = 'pdb1050.awardspace.net'; // تغيير إلى المضيف الخاص بك
$dbname = '4438085_devadnan'; // اسم قاعدة البيانات
$username = '4438085_devadnan'; // اسم المستخدم لقاعدة البيانات
$password = 'Adnan&&123'; // كلمة المرور لقاعدة البيانات

// إنشاء الاتصال بقاعدة البيانات
try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    // ضبط إعدادات PDO لمعالجة الأخطاء
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
    exit;
}

// قراءة البيانات المستلمة عبر POST
$data = json_decode(file_get_contents("php://input"), true);

// التحقق من أن البيانات موجودة
if (isset($data['title']) && isset($data['content']) && isset($data['audio_url'])) {
    $title = $data['title'];
    $content = $data['content'];
    $audio_url = $data['audio_url'];

    // جملة SQL لإدخال البيانات في جدول `episodes`
    $sql = "INSERT INTO episodes (title, content, episode_url) VALUES (:title, :content, :episode_url)";

    // إعداد الاستعلام
    $stmt = $pdo->prepare($sql);

    // ربط المعلمات بالبيانات
    $stmt->bindParam(':title', $title);
    $stmt->bindParam(':content', $content);
    $stmt->bindParam(':episode_url', $audio_url);

    // تنفيذ الاستعلام
    if ($stmt->execute()) {
        // إرسال استجابة بنجاح
        echo json_encode(["status" => "success", "message" => "Data inserted successfully."]);
    } else {
        // إرسال استجابة بالفشل
        echo json_encode(["status" => "error", "message" => "Failed to insert data."]);
    }
} else {
    // إذا كانت البيانات غير مكتملة، أرسل رسالة خطأ
    echo json_encode(["status" => "error", "message" => "Invalid data received."]);
}

?>
